
def get_current_student_list():
    student_db = [{"studentId": "aaaa","name":"Alice Alpha","emails":"alice@gprof.com","meetingName":"1:1 Alice"},
          {"studentId": "bbbb","name":"Bob Beta","emails":"bob@gprof.com","meetingName":"1:1 Alice"},
          {"studentId": "cccc","name":"Charlie Christ","emails":"charlie@gprof.com","meetingName":"1:1 Charlie "},
        ]
    full_response="Here is the student list:\n\n"
    for s in student_db:
        full_response += f"Name: {s['name']}, Meeting: {s['meetingName']}, Emails: {s['emails']}\n"
    return full_response