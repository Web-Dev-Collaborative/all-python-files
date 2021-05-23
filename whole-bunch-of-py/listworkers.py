import json
import sys
import os
import urllib.request


def main():
    rootUrl = os.environ["TASKCLUSTER_ROOT_URL"]
    workerPoolId = sys.argv[1]
    apiUrl = rootUrl + "/api/worker-manager/v1/workers/" + workerPoolId
    continuationToken = None

    while True:
        url = apiUrl + "?limit=100"
        if continuationToken:
            url += "&continuationToken={}".format(continuationToken)
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read())
            for worker in data["workers"]:
                print(json.dumps(worker, sort_keys=True, indent=4))
            if "continuationToken" in data:
                continuationToken = data["continuationToken"]
            else:
                break


main()
