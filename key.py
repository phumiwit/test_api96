from tensorflow import keras
import numpy as np
import librosa
from pydub import AudioSegment


MODEL_PATH = 'Music_Genre_10_CNN2.h5'
NUM_SAMPLES_TO_CONSIDER = 22050
TRACK_DURATION = 30 # measured in seconds
SAMPLES_PER_TRACK = NUM_SAMPLES_TO_CONSIDER * TRACK_DURATION
num_segments = 10
class _Keyword_Spotting_Service:
    model = None
    _mappings = [
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock"
    ]
    _instance = None
    
   



    def segment(self,filepath):
       waveFile  = []
       cut0 = 0
       cut1 = 30000
       waveFile1 = AudioSegment.from_file(filepath)
       for j in range(round((len(waveFile1)/30000))):
        if cut1+30000 < len(waveFile1):
          waveFile.append(waveFile1[cut0:cut1])
          print('Round' + str(j+1))
          cut0 += 30000
          cut1 += 30000
          
       waveFile.append(waveFile1[cut0:cut1])
       print('Round' + str(j+1))
       cut0 += 30000
       cut1 = len(waveFile1)
       waveFile.append(waveFile1[cut0:cut1])
       return waveFile
    
    def Export(self,x):
        song = []
        for i in range(len(x)):
            song.append(x[i].export('audio_sample_30s' + str(i) +  '.wav' , format="wav"))
       
        return song
    
    
    def MFCC(self,file_path):
        song_30 = []
        x = self.segment(file_path)
        x1 = self.Export(x)
        for i in range(len(x1)):
            MFCCs = self.preprocess(x1[i],30)
            MFCCs = MFCCs[np.newaxis, ...,np.newaxis]
            song_30.append(MFCCs)
        return song_30
    
    
    def prediction(self,song_30):
        genre = [
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock"
    ]
        song_30 = self.MFCC(song_30)
        save_genre = []
        MFCC_FOR_PLOT = {}
        value = []
        k = 0
        for i in range(len(song_30)):
            predictions =self.model.predict(song_30[i])
            predicted_index = np.argmax(predictions)
            predicted_keyword = self._mappings[predicted_index]
            save_genre.append(predicted_keyword)
            for j in range(10):
                MFCC_FOR_PLOT[genre[j] + str(k)] = str(predictions[0][j])
            k += 1
        
        keyword = max(save_genre,key = save_genre.count)
        return keyword,MFCC_FOR_PLOT
    
    
        
    
    def preprocess(self,file_path,duration,n_mfcc=13,n_fft=2048,hop_length=512):
        SAMPLE_RATE = 22050
        TRACK_DURATION =  duration# measured in seconds
        SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
        NUM_SEGMENTS = 10
        samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
        signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)
        
        for d in range(10):

          # calculate start and finish sample for current segment
          start = samples_per_segment * d
          finish = start + samples_per_segment

          # extract mfcc
          mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
          print(mfcc)
          #mfcc = mfcc.T

          return mfcc.T
      
    
    
def Keyword_Spotting_Service():
    if _Keyword_Spotting_Service._instance is None:
        _Keyword_Spotting_Service._instance = _Keyword_Spotting_Service()
        _Keyword_Spotting_Service.model = keras.models.load_model(MODEL_PATH)
    return _Keyword_Spotting_Service._instance