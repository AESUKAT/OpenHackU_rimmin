import librosa
import numpy as np
import soundfile as sf
import moviepy.editor as mp
from pytube import YouTube

# 音圧偏差値70以上の区間をリストにして返す
def dB_determination(YouTube_URL):

    mp4_file_path = 'load_mp4.mp4'
    wav_file_path = 'wav_file.wav'
    download(YouTube_URL, mp4_file_path)
    mp4_to_wav(mp4_file_path, wav_file_path)

    volume_dB_mean_overstn, new_times = voloume_dB_mean_per_seconds(wav_file_path)
    time_index = volume_dB_value_cal(volume_dB_mean_overstn)

    start_time_list, end_time_list = start_end_timing(new_times, time_index)

    chapter_list = create_chapter_list(start_time_list, end_time_list)

    print('全完')
    return chapter_list

# 動画をダウンロードする
def download(Video_URL, mp4_file_path):
    video = YouTube(Video_URL).streams.filter(subtype='mp4').first()
    video.download('./', mp4_file_path)
    print('DL完了')

# mp4ファイルをモノラル音声のwavファイルに変換する
def mp4_to_wav(mp4_file_path, wav_file_path):
    video = mp.VideoFileClip(mp4_file_path)
    audio = video.audio
    audio.write_audiofile(wav_file_path)

    sound, fs = sf.read(wav_file_path)
    mono_data = sound if type(sound[0]) is float else stereo_to_mono(sound)
    sf.write(wav_file_path, mono_data, fs)

    print('WAV変換完了')

# ステレオ音声をモノラル音声に変える
def stereo_to_mono(stereo_data):
    mono_data = np.array([float(0)]*len(stereo_data))
    mono_data += np.mean(stereo_data, axis=1)
    print('mono化完了')
    return mono_data

# 音圧を1秒あたりの平均値にまとめる
def voloume_dB_mean_per_seconds(wav_file_path):
    sound, fs = sf.read(wav_file_path)
    rms = librosa.feature.rms(y=sound)
    volume_dB = 20 * np.log10(rms[0])

    volume_dB_mean = np.array([])
    seconds = 1

    volume_dB = np.delete(volume_dB, slice(None, None, 500))

    for i in range(1, len(volume_dB), 86):
        volume_dB_mean = np.append(volume_dB_mean, [np.mean(volume_dB[i:i+86]), seconds])
        seconds += 1

    volume_dB_mean_overstn = np.array([])
    new_times = np.array([])

    for i in range(0,len(volume_dB_mean),2):
        if volume_dB_mean[i] > -30:
            volume_dB_mean_overstn = np.append(volume_dB_mean_overstn, volume_dB_mean[i])
            new_times = np.append(new_times, volume_dB_mean[i+1])
    
    print('音圧毎秒平均完了', seconds)
    return volume_dB_mean_overstn, new_times

# 音圧の区間あたりの偏差値と高偏差値の時間を出す
def volume_dB_value_cal(volume_dB_mean_overstn):
    volume_dB_mean_mean = np.mean(volume_dB_mean_overstn)
    volume_dB_std = np.std(volume_dB_mean_overstn)
    volume_dB_value = 50 + ((volume_dB_mean_overstn - volume_dB_mean_mean) / volume_dB_std) * 10

    deviation = 70
    time_index = np.where(volume_dB_value >= deviation)

    print('うるさい時間検索完了')
    return time_index

# 再生時間と再生終了時間を調べる
def start_end_timing(new_times, time_index):
    time_wid = 2

    for i in range(len(time_index)):
        np_start_time = new_times[time_index[i]] - time_wid
        np_end_time = new_times[time_index[i]] + time_wid
    start_time_list = np_start_time.tolist()
    end_time_list = np_end_time.tolist()

    print('再生する時間の探索完了')
    return start_time_list, end_time_list

# 再生するチャプターリストを作成
def create_chapter_list(start_time_list, end_time_list):
    len_start_end_time_list = len(start_time_list)

    start_flag = False
    end_flag = False
    chapter_list = list()

    for i in range(len_start_end_time_list):
        if not start_flag:
            start_flag = True
            start_time = int(start_time_list[i])
        if start_flag:
            if i < len_start_end_time_list-1:
                if end_time_list[i] > start_time_list[i+1]:
                    pass
                else:
                    end_flag = True
                    end_time = int(end_time_list[i])
            else:
                end_flag = True
                end_time = int(end_time_list[i])
        if end_flag:
            start_flag = False
            end_flag = False
            if (end_time - start_time > 5):
                chapter_list.append([start_time, end_time])
    
    print('チャプターリスト作成完了')
    return chapter_list

chapter_list = dB_determination('https://www.youtube.com/watch?v=EYYizyYe5GY')