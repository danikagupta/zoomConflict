# Mock Zoom API

hosts={
   "14FZQXqLRSODS33uQTVVaw":["Zoom 1",1111],
   "5uBBBmxkRs2ULd5cfs8Adw":["Zoom 2",22222],
   "atAAAIDOQYqcONrWd0oxxg":["Zoom 3",33333],
   "dZ6K_rnJTOO5S-jOUpXf3w":["Zoom 4",44444],
   "j4IclWA4ScOUmP_grnbflg":["Zoom 5",55555],
}

def get_zoom_name(host_id):
    if host_id in hosts:
        return hosts[host_id][0]
    return host_id

def get_zoom_code(host_id):
    if host_id in hosts:
        return hosts[host_id][1]
    print(f"Cannot find host-id {host_id} and the return value is {-1*int(host_id)}")
    return -1*int(host_id)

def get_scheduled_zoom_api_response():
    resp = {
        "upcoming": {
                    "sessions": [
                            {
                            "uuid": "oB0lfCbPQTKMyhRjb+4IIw==",
                            "id": 84036842404,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Samvrith Bandi (06/16)",
                            "type": 2,
                            "start_time": "2024-06-17T03:30:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-14T08:32:40Z",
                            "join_url": "https://us02web.zoom.us/j/84036842404?pwd=t4smvVkpAaxgb7DYPf6yCDo6QxTibi.1"
                        },
                        {
                            "uuid": "jkpzjGxuRZ6m3KDUuxciJQ==",
                            "id": 82342598986,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "SC_M1_06_17_24_Ms. Neeta A.N",
                            "type": 8,
                            "start_time": "2024-06-17T16:30:00Z",
                            "duration": 180,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-10T05:37:43Z",
                            "join_url": "https://us02web.zoom.us/j/82342598986?pwd=PQasbymJdzJIyWJ0xVbi1vsF7e3J9k.1"
                        },
                        {
                            "uuid": "5AoQq/vjQhC8Pco0Np2vBQ==",
                            "id": 88675950630,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": " AI/ML training for Trane Cohort 1",
                            "type": 8,
                            "start_time": "2024-06-17T18:30:00Z",
                            "duration": 90,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-05-25T03:20:01Z",
                            "join_url": "https://us02web.zoom.us/j/88675950630?pwd=bkbMGtDvadS3lakNTj9S1PEvQ39sK0.1"
                        },
                        {
                            "uuid": "egrEuS7tRAidzvk7FxRQGw==",
                            "id": 85884479408,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Anisha",
                            "type": 8,
                            "start_time": "2024-06-17T23:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-07-29T13:32:36Z",
                            "join_url": "https://us02web.zoom.us/j/85884479408?pwd=OExvT2JVazdXVUdMQWxuOE1xb28vZz09"
                        },
                        {
                            "uuid": "ytrqemtmSfWn5a4ZPUCmjg==",
                            "id": 89997861032,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Mouli Banga",
                            "type": 8,
                            "start_time": "2024-06-17T23:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-09T05:28:38Z",
                            "join_url": "https://us02web.zoom.us/j/89997861032?pwd=KAIAlFcBqa9YZpKCbXuNpMNTTWgx7u.1"
                        },
                        {
                            "uuid": "QWYGRQ9WToSuK2Pm/5o8lQ==",
                            "id": 86282797155,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Anisha",
                            "type": 8,
                            "start_time": "2024-06-18T00:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-05-21T03:22:16Z",
                            "join_url": "https://us02web.zoom.us/j/86282797155?pwd=WXppb252WElQSXl5UWdCaFBrQWFSZz09"
                        },
                        {
                            "uuid": "DMiKJdC9SOiSE3S9eaSCPw==",
                            "id": 89465161555,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Emmett Chen",
                            "type": 8,
                            "start_time": "2024-06-18T03:45:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-04-19T09:59:13Z",
                            "join_url": "https://us02web.zoom.us/j/89465161555?pwd=bllmSVhBM1QzWkozM09maVRPVmJrZz09"
                        },
                        {
                            "uuid": "jkpzjGxuRZ6m3KDUuxciJQ==",
                            "id": 82342598986,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "SC_M1_06_17_24_Ms. Neeta A.N",
                            "type": 8,
                            "start_time": "2024-06-18T16:30:00Z",
                            "duration": 180,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-10T05:37:43Z",
                            "join_url": "https://us02web.zoom.us/j/82342598986?pwd=PQasbymJdzJIyWJ0xVbi1vsF7e3J9k.1"
                        },
                        {
                            "uuid": "p/v/Dw4JQQqUA0oHLUts5w==",
                            "id": 86038165846,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Pranav Goel_Dr.Ghanta",
                            "type": 8,
                            "start_time": "2024-06-18T22:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-06-29T04:39:45Z",
                            "join_url": "https://us02web.zoom.us/j/86038165846?pwd=T1dCVUMvU3Y4VVlMWWhON3NrZzRVUT09"
                        },
                        {
                            "uuid": "YXzKjBx3RL+1y04A/GO18A==",
                            "id": 81545959304,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Sriteja Kataru_Dr.Sindhu Ghanta",
                            "type": 8,
                            "start_time": "2024-06-19T03:30:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-01-26T18:34:18Z",
                            "join_url": "https://us02web.zoom.us/j/81545959304?pwd=NmZpV1FiVHRVNkxBZy80WDJ6Rnlodz09"
                        },
                        {
                            "uuid": "jkpzjGxuRZ6m3KDUuxciJQ==",
                            "id": 82342598986,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "SC_M1_06_17_24_Ms. Neeta A.N",
                            "type": 8,
                            "start_time": "2024-06-19T16:30:00Z",
                            "duration": 180,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-10T05:37:43Z",
                            "join_url": "https://us02web.zoom.us/j/82342598986?pwd=PQasbymJdzJIyWJ0xVbi1vsF7e3J9k.1"
                        },
                        {
                            "uuid": "uc4XeFvzQQqub4NI43cjfQ==",
                            "id": 81082075674,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Avijay",
                            "type": 8,
                            "start_time": "2024-06-19T23:30:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-02-05T07:06:01Z",
                            "join_url": "https://us02web.zoom.us/j/81082075674?pwd=NndINVh6V053TkhjU3FPZTcwd1EyZz09"
                        },
                        {
                            "uuid": "rGVNq7jYSGupDGhLtoT/eQ==",
                            "id": 85140303633,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "M1_06_05_24_Mr. Sreenath P.L",
                            "type": 8,
                            "start_time": "2024-06-20T00:00:00Z",
                            "duration": 90,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-05-29T12:38:16Z",
                            "join_url": "https://us02web.zoom.us/j/85140303633?pwd=ZVeOz5HQYsHn8rmTaEcUTSaYnxxzT3.1"
                        },
                        {
                            "uuid": "gVvj8vKjTGe+1lDF5bX7DA==",
                            "id": 84422920447,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "M1_05_15_24_Ms. Neeta",
                            "type": 8,
                            "start_time": "2024-06-20T02:00:00Z",
                            "duration": 90,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-04-22T08:34:31Z",
                            "join_url": "https://us02web.zoom.us/j/84422920447?pwd=VkNwYno0bitxbWg5RHYyUGRWZjYrZz09"
                        },
                        {
                            "uuid": "XZqzntOuSuy6pJvhsFnQOQ==",
                            "id": 85062797377,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Disha Gupta_Mr.Lachin",
                            "type": 8,
                            "start_time": "2024-06-20T02:30:00Z",
                            "duration": 30,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-03-01T05:56:51Z",
                            "join_url": "https://us02web.zoom.us/j/85062797377?pwd=VVNESk8rQmNiN0ppVEtFR2tzeFAyUT09"
                        },
                        {
                            "uuid": "TsZ3ZQ6+R2GNcy7ZGkGQUw==",
                            "id": 82436731931,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Neha Shaik_ Wednesday Sessions",
                            "type": 8,
                            "start_time": "2024-06-20T03:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-08-01T04:07:29Z",
                            "join_url": "https://us02web.zoom.us/j/82436731931?pwd=RUozZTl1aEwrWmt4c3hKUmlMMTY3Zz09"
                        },
                        {
                            "uuid": "jkpzjGxuRZ6m3KDUuxciJQ==",
                            "id": 82342598986,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "SC_M1_06_17_24_Ms. Neeta A.N",
                            "type": 8,
                            "start_time": "2024-06-20T16:30:00Z",
                            "duration": 180,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-06-10T05:37:43Z",
                            "join_url": "https://us02web.zoom.us/j/82342598986?pwd=PQasbymJdzJIyWJ0xVbi1vsF7e3J9k.1"
                        },
                        {
                            "uuid": "ObGzZ9sdQpqbR3dENKzN1g==",
                            "id": 89604664865,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Giselle Drewett",
                            "type": 8,
                            "start_time": "2024-06-20T17:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-05-14T05:22:01Z",
                            "join_url": "https://us02web.zoom.us/j/89604664865?pwd=ZEFSTkZienlwMDhJUmMzNE95a2dNdz09"
                        },
                        {
                            "uuid": "E2g2gTUSSCKG0aum3TZXbg==",
                            "id": 89488533682,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Neel Dhuruva",
                            "type": 8,
                            "start_time": "2024-06-20T22:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-12-28T06:22:16Z",
                            "join_url": "https://us02web.zoom.us/j/89488533682?pwd=VzJBcjJCaGxpVWFESmpaOGlTNUovUT09"
                        },
                        {
                            "uuid": "OeXhWoNfSJaq5YBBwEgCGw==",
                            "id": 89898564836,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Anik Sahai",
                            "type": 8,
                            "start_time": "2024-06-21T00:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-11-29T04:49:30Z",
                            "join_url": "https://us02web.zoom.us/j/89898564836?pwd=eWhBSis2QU9hYzd6MVllaWFDaFl4dz09"
                        },
                        {
                            "uuid": "83HKPveURrauRSfUgn5SQQ==",
                            "id": 84608408989,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Shriya Shukla",
                            "type": 8,
                            "start_time": "2024-06-21T01:30:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-11-23T06:12:30Z",
                            "join_url": "https://us02web.zoom.us/j/84608408989?pwd=OXlocjdtVXdEK1VlMGpRZlFvNUVqUT09"
                        },
                    ],
                    "total_sessions": 1
                }
    }
    return resp

def get_current_zoom_api_response():
    resp = {
        "live": {
                    "sessions": [
                        {
                            "uuid": "dOt7Crc5R32M1aibgo8Y0g==",
                            "id": 86050250486,
                            "host_id": "dZ6K_rnJTOO5S-jOUpXf3w",
                            "topic": "1:1 Caitlin Dosch",
                            "type": 3,
                            "start_time": "2024-06-02T16:30:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2024-03-16T17:13:01Z",
                            "join_url": "https://XXXXXus02web.zoom.us/j/86050250486?pwd=UWZHb0lDeUwxOXJrTlBwZHd6dXBkdz09"
                        },
                        {
                            "uuid": "E2g2gTUSSCKG0aum3TZXbg==",
                            "id": 89488533682,
                            "host_id": "14FZQXqLRSODS33uQTVVaw",
                            "topic": "1:1 Neel Dhuruva",
                            "type": 8,
                            "start_time": "2024-06-20T22:00:00Z",
                            "duration": 60,
                            "timezone": "America/Los_Angeles",
                            "created_at": "2023-12-28T06:22:16Z",
                            "join_url": "https://XXXXXXus02web.zoom.us/j/89488533682?pwd=VzJBcjJCaGxpVWFESmpaOGlTNUovUT09"
                        },
                    ],
                    "total_sessions": 1
                }
    }
    return resp


def get_current_sessions():
  zoom_sessions=get_current_zoom_api_response()
  sessions = zoom_sessions['live']['sessions']
  response=f"We currently have {len(sessions)} live sessions.\n"
  for s in sessions:
     response+=f"* Title: {s['topic']}, Host: {get_zoom_name(s['host_id'])}, URL: {s['join_url']}\n"
  return response

def get_scheduled_sessions():
  zoom_sessions=get_scheduled_zoom_api_response()
  print(f"Scheduled sessions. Zoom-sessions = {zoom_sessions}")
  sess = zoom_sessions['upcoming']['sessions']
  print(f"Sessions: {sess}")
  resp = "Scheduled sessions:\n"
  for s in sess:
    resp+=f"Title = {s['topic']}, Login = {get_zoom_name(s['host_id'])}\n"
  #resp = str([f"User = {get_zoom_name(s['host_id'])}, Title = {s['topic']}\n" for s in sess])
  return resp

def get_host_code(host_id):
  return get_zoom_code(host_id)

def get_zoom_table():
  response = "\n Zoom Cancel Codes are:\n"
  for k,v in hosts.items():
    response+=f"Host: {v[0]}, Code: {v[1]}\n"
  return response+"\n\n"