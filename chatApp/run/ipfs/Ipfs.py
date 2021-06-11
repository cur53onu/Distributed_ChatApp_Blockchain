import ipfsApi


class IpfsHandle:
    def __init__(self):
        self.api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)

    def catFile(self, fhash):
        print(self.api.cat(fhash))

    def addFile(self, filepath):
        obj = self.api.add(filepath)
        print(obj)
