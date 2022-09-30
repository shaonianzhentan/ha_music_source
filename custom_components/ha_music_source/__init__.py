from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .manifest import manifest
from musicdl import musicdl

DOMAIN = manifest.domain

CONFIG_SCHEMA = cv.deprecated(DOMAIN)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data['ha_music_source'] = MusicSource(hass)
    return True

class MusicSource():

    def __init__(self, hass):
        self.hass = hass

    # 搜索音乐
    async def async_search(self, name, size=1):

        config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': size, 'proxies': {}}
        target_srcs = [
            'kugou', 'kuwo', 'qqmusic', 'qianqian', 'fivesing', 'migu', 'joox', 'yiting',
        ]
        client = musicdl.musicdl(config=config)

        search_results = await self.hass.async_add_executor_job(client.search, name, target_srcs)

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
        return music_list

    # 获取音乐链接
    async def async_song_url(self, song, singer):
        music_list = await self.async_search(f'{song} - {singer}')
        if len(music_list) > 0:
            # 精确匹配
            for item in music_list:
                if song in item['song'] and singer in item['singer']:
                    return item['url']

            music = music_list[0]
            return music['url']