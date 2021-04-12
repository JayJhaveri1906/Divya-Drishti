import os
path = os.path.dirname(os.path.abspath(__file__))

common_job_titles = []

with open(path + '/../data/common_job_name', encoding="utf8") as common_job_names:
    for job_name in common_job_names:
        job_name = job_name.strip().lower()
        if len(job_name) > 0:
            common_job_titles.append(job_name)


def is_job_title(line):
    line = line.lower()
    for title in common_job_titles:
        if line.find(title) >= 0:
            return True
    return False