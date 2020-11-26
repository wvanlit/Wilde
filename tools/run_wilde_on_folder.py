import glob
import click
import os
import time
import datetime
import subprocess

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--file_type', '-t', type=click.Choice(['mp3','wav']), default='mp3', help='The file format. Defaults to mp3.')
def run_on_folder(path, file_type):
    path = click.format_filename(path)
    print(f'> Running on all {file_type} files in \'{path}\'')
    
    # go to path
    os.chdir(path)
    root = os.getcwd()
    files = glob.glob(f'*.{file_type}') 
    start = time.time()
    for index, audio_file in enumerate(files):
        # Get name for folder
        audio_name = audio_file.split('.')[0].replace(' ', '_')
        output_folder_path = os.path.join(root, audio_name+'/')
        
        # if directory already exists then tool has already done this > Skip it
        if os.path.isdir(output_folder_path):
            print(f'> Skipping \'{audio_file}\' since it already has a folder')
            continue
        
        # create output dir
        os.mkdir(output_folder_path)

        # run Wilde
        cmd_args = [
            'wilde', 
            audio_file,
            '--output',
            output_folder_path,
            '-t',
            file_type,
        ]
        process = subprocess.run(cmd_args)

        if process.returncode != 0:
            print(f'> Error during the processing of {audio_name}')
    
        # Status
        elapsed = str(datetime.timedelta(seconds=(time.time()-start)))
        print(f'> Status: {index+1}/{len(files)} done. Time spent: {elapsed}')

        

if __name__ == '__main__':
    run_on_folder()

