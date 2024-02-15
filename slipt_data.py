import re
from datetime import datetime

def read_vtt_file(file_path):
    subtitle_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if re.match(r'^\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}$', line):
                start, end = line.split(' --> ')
                start_time = datetime.strptime(start, '%H:%M:%S.%f')
                end_time = datetime.strptime(end, '%H:%M:%S.%f')

                # Get content inside <v> tag
                content = lines[index + 1].strip()
                match = re.search(r'<v.*?>(.*?)</v>', content)
                if match:
                    speaker_match = re.search(r'<v\s+([A-Za-z\s]+?)\s*>', match.group(0))
                    if speaker_match:
                        subtitle_text = match.group(1)
                        subtitle_list.append({
                            'start_time': start_time,
                            'end_time': end_time,
                            'speaker' : speaker_match.group(1),
                            'content': subtitle_text
                        })
                index += 1  # skip next line
            index += 1

    return subtitle_list

# Example usage
file_path = 'R&D DailyMTG_2024-02-05.vtt'
subtitles = read_vtt_file(file_path)

for subtitle in subtitles:
    print(f"Thời gian: {subtitle['start_time']} - {subtitle['end_time']}")
    print(f"{subtitle['speaker']}: {subtitle['content']}")
    print()
