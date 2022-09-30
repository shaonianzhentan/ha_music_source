from musicdl import musicdl

def search(name):

    config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 1, 'proxies': {}}
    target_srcs = [
        'kugou', 'kuwo', 'qqmusic', 'qianqian', 'fivesing', 'migu', 'joox', 'yiting',
    ]
    client = musicdl.musicdl(config=config)
    search_results = client.search(name, target_srcs)

    music_list = []
    for key, value in search_results.items():
        if len(value) > 0:
            item = value[0]
            if item['ext'] == 'mp3':
                music_list.append({
                    'song': item['songname'],
                    'singer': item['singers'],
                    'album': item['album'],
                    'url': item['download_url']
                })
                print(music_list[len(music_list) - 1])

    return music_list

        
def song_url(song, singer):
    music_list = search(f'{song} - {singer}')
    if len(music_list) > 0:
        # 精确匹配
        for item in music_list:
            if song in item['song'] and singer in item['singer']:
                return item['url']
        
        music = music_list[0]
        return music['url']

print(song_url('爱要怎么说出口', '赵传'))