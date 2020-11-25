import click
import logging
import os

from pydub import AudioSegment
from inaSpeechSegmenter import Segmenter

TEMPORARY_FOLDER_NAME = 'tmp/'


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--file_type', '-t', type=click.Choice(['mp3','wav']), default='mp3', help='The file format. Defaults to mp3.')
@click.option('--size', '-s', default=600, help='Segmentation size in seconds. Defaults to 600.')
@click.option('--output', '-o', type=click.Path(exists=True), default='.', help='Path for the output files.')
@click.option('--verbose', '-v', default=True, help='Output verbose logging information.')
def find_music_in_file(path, file_type, size, output, verbose):
    logging_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging_level)

    # Segment audio
    audio_segments = segment_audio(click.format_filename(path), file_type, size)
    audio_files = export_segments_to_files(audio_segments, file_type, click.format_filename(output))

    # Detect music fragments
    music_segments = extract_music_from_segments(audio_files)

    # Export music fragments
    export_music_segments(music_segments, output)

    # Cleanup
    remove_temporary_folder(output)

def segment_audio(path, file_type, size_in_seconds):
    size_in_milliseconds = size_in_seconds * 1000

    logging.info('Starting audio segmentation')
    logging.info('Retrieving audio file')
    full_file = get_audio_segment_from_file(path, file_type)    

    logging.info(f'Splitting audio file in segements of {size_in_milliseconds}ms')
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
        logging.info('Creating temporary folder')
        os.makedirs(temporary_folder_path)
        
    logging.info('Exporting audio chunks to temporary folder')
    file_names = []
    for index, audio in enumerate(segments):
        file_name = os.path.join(temporary_folder_path, f'chunk-{index}.{file_type}')
        audio.export(file_name, format=file_type)
        file_names.append(file_name)
    return file_names

def extract_music_from_segments(audio_files):
    music_segments = []
    for audio in audio_files:
        pass

def export_music_segments(music_segments, output_path):
    pass

def remove_temporary_folder(output_path):
    temporary_folder_path = os.path.join(output_path, TEMPORARY_FOLDER_NAME)
    if os.path.exists(temporary_folder_path):
        logging.info('Remove temporary folder')
        os.rmdir(temporary_folder_path)

if __name__ == '__main__':
    find_music_in_file()
