from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=RuntimeWarning)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import click
import shutil
from datetime import datetime
from pydub import AudioSegment
from inaSpeechSegmenter import Segmenter

TEMPORARY_FOLDER_NAME = 'tmp/'
verbose_logging = None

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--file_type', '-t', type=click.Choice(['mp3','wav']), default='mp3', help='The file format. Defaults to mp3.')
@click.option('--size', '-s', default=600, help='Segmentation size in seconds. Defaults to 600.')
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Path for the output files.')
@click.option('--verbose', '-v', is_flag=True, help='Output verbose logging information.')
@click.option('--minimal_duration', '-md', default=5, help='Minimal duration music has t be when exporting')
@click.option('--join_distance', '-jd', default=5, help='The maximum time between joined segments')
def find_music_in_file(path, file_type, size, output, verbose, minimal_duration, join_distance):
    global verbose_logging
    verbose_logging = verbose

    # Segment audio
    audio_segments = segment_audio(click.format_filename(path), file_type, size)
    audio_files = export_segments_to_files(audio_segments, file_type, click.format_filename(output))

    # Detect music fragments
    music_segments = extract_music_from_segments(audio_files, size)
    joined_music_segments = join_nearby_segments(music_segments, distance_in_seconds=join_distance)
    # Export music fragments
    export_music_segments(
            joined_music_segments, 
            click.format_filename(path), 
            file_type, 
            click.format_filename(output),
            minimal_duration=minimal_duration,
    )

    # Cleanup
    remove_temporary_folder(output)

    log('Finished execution', verbose=False)

def segment_audio(path, file_type, size_in_seconds):
    size_in_milliseconds = size_in_seconds * 1000

    log('Starting audio segmentation', verbose=False)
    log('Retrieving audio file')
    full_file = get_audio_segment_from_file(path, file_type)    

    log(f'Splitting audio file in segements of {size_in_milliseconds}ms')
    return split_audio_segment(full_file, size_in_milliseconds)

def get_audio_segment_from_file(path, file_type):
    if file_type == 'mp3':
        return AudioSegment.from_mp3(path)
    elif file_type == 'wav':
        return AudioSegment.from_wav(path)
    else:
        raise NotImplementedError(f'Audio segmenting for {file_type} is not implemented')

def split_audio_segment(input_audio, segment_size):
    if len(input_audio) <= segment_size:
        return [input_audio]

    return input_audio[::segment_size]

def export_segments_to_files(segments, file_type, output_path):
    temporary_folder_path = os.path.join(output_path, TEMPORARY_FOLDER_NAME)
    if not os.path.exists(temporary_folder_path):
        log('Creating temporary folder')
        os.makedirs(temporary_folder_path) 
    log('Exporting audio chunks to temporary folder', verbose=False)
    file_names = []
    for index, audio in enumerate(segments):
        file_name = os.path.join(temporary_folder_path, f'chunk-{index+1}.{file_type}')
        audio.export(file_name, format=file_type)
        file_names.append(file_name)
        log(f'{file_name} exported')
    log('Exporting done', verbose=False)
    return file_names

def extract_music_from_segments(audio_files, segment_size):
    log('Starting music classification', verbose=False)
    seg = Segmenter(vad_engine='sm', detect_gender=False)
    music_segments = []
    for index, audio in enumerate(audio_files):
        segmentation = seg(audio)
        for (seg_type, start, end) in segmentation:
            if seg_type == 'music':
                offset = index*segment_size
                music_segments.append((int(start+offset), int(end+offset)))
        log(f'Chunk {index+1} out of {len(audio_files)} classified...')
    log('Classification done', verbose=False)
    return music_segments

def join_nearby_segments(music_segments, distance_in_seconds=5):
    joined_segments = []
    for index, (start, end) in enumerate(music_segments):
        if index != 0:
            prev_end = joined_segments[:-1][1]
            if prev_end+distance_in_seconds > start:
                joined_segments[:-1][1] = end
            else:
                joined_segments.append((start, end))
        else:
            joined_segments.append((start, end))

def export_music_segments(music_segments, audio_path, file_type, output_path, minimal_duration=5): 
    log('Starting music segment export', verbose=False)
    full_file = get_audio_segment_from_file(audio_path, file_type)
    for index, (start, end) in enumerate(music_segments):
        if end-start < minimal_duration:
            log(f'Skipping export of music between {start} and {end}')
            continue
        start_ms = int(start*1000)
        end_ms = int(end*1000)
        segment = full_file[start_ms:end_ms]
        
        filename = f'export_{start}_{end}.{file_type}'
        filepath = os.path.join(output_path, filename)
        
        segment.export(filepath, format=file_type)
        log(f'Exported {filename}')

def remove_temporary_folder(output_path):
    temporary_folder_path = os.path.join(output_path, TEMPORARY_FOLDER_NAME)
    if os.path.exists(temporary_folder_path):
        log('Removing temporary folder')
        shutil.rmtree(temporary_folder_path)

def log(text, verbose=True):
    """Custom logging since tensorflow interfers with python logging"""
    dateObj = datetime.now()
    timestamp = f'[{dateObj.hour:0>2d}:{dateObj.minute:0>2d}:{dateObj.second:0>2d}]'
    if (verbose and verbose_logging is True) or not verbose:
        print(f'{timestamp} {text}')

if __name__ == '__main__':
    find_music_in_file()
