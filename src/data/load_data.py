import wget
from zipfile import ZipFile

def get_data(source, file_path, file):
  wget.download(source, file_path)
  print('downloaded')

  # opening the zip file in READ mode
  with ZipFile(file, 'r') as zip:
    
      # extracting all the files
      print('Extracting all the files now...')
      zip.extractall(file_path)
      print('Done!')
