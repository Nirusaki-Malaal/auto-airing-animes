import aiohttp , requests
class Aria2py:
    
    async def add_magnet(self,magnet: str, out_dir:str , out_name:str):
        url = "http://localhost:6800/jsonrpc"
        async with aiohttp.ClientSession() as session:
            async with session.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": "1",
                "method": "aria2.addUri",
                "params": [
                    [magnet],
                    {
                        "dir": out_dir,
                        "out" : out_name,
                        "seed-time": "0",
                        "follow-torrent": "true"
                    }
                ]
            }
        ) as resp:
             data = await resp.json()
             return data['result'] ## gid
    def tell_status(self, gid):
        url = "http://localhost:6800/jsonrpc"
        payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "aria2.tellStatus",
        "params": [gid]
        }
        res = requests.post(url, json=payload)
        return res.json()['result']
    
    def real_gid(self, meta_gid):
        while True:
            data = self.tell_status(meta_gid)
            # Metadata finished → real download created
            if "followedBy" in data and data["followedBy"]:
                return data["followedBy"][0] ## real_gid
    
    async def add_batch(self,magnet: str, out_dir:str):
        url = "http://localhost:6800/jsonrpc"
        async with aiohttp.ClientSession() as session:
            async with session.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": "1",
                "method": "aria2.addUri",
                "params": [
                    [magnet],
                    {
                        "dir": out_dir,
                        "seed-time": "0",
                        "follow-torrent": "true"
                    }
                ]
            }
        ) as resp:
             data = await resp.json()
             return data['result'] ## gid

    
    
