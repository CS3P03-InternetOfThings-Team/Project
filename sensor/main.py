import requests
import uuid
import os
import threading
import time

start = time.time()

files_to_process = []


def process_recordings(event):
    while True:
        if (len(files_to_process) == 0):
            print('No files to process. Sleeping until there is at least one')
            event.wait()  # wait for signal that there are more files to process
            print('Woke up!')
            event.clear()  # clear signal for future use

        file_to_process = files_to_process[0]

        if file_to_process == 'HALT':
            break

        print(f'Processing {file_to_process}')
        try:
            # process 1st file on the list
            with open(file_to_process, 'rb') as wavFile:
                print('Sending recording to backend')
                res = requests.post('http://192.168.1.42:3000/uploads/audio', params={
                    'username': 'Gabriel Spranger',
                    'timestamp': round(time.time() - start, 2),
                }, files={
                    'audio': (filename, wavFile, 'audio/wav')
                })
                data = res.json()

                print('Recording sent. Backend response: ', data)
        except FileNotFoundError:
            print(f'File "{file_to_process}" not found. Trying again...')
            continue  # try reading the file again

        # file has been processed to remove it from pending list
        files_to_process.pop(0)
        os.remove(file_to_process)


wake_up_event = threading.Event()

processing_thread = threading.Thread(
    target=process_recordings, args=(wake_up_event,))

processing_thread.start()

for _ in range(5):
    filename = f'{uuid.uuid4()}.wav'
    command = f'arecord -q -f S16_LE -r 44100 -c 1 -D plughw:3,0 -d 5 -t wav -v {filename}'
    os.system(command)
    print(f'Appending {filename}')
    files_to_process.append(filename)
    wake_up_event.set()

files_to_process.append('HALT')

processing_thread.join()  # wait for processing thread to finish
