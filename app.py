from flask import Flask, request, jsonify
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

machine = []

#1.Register a machine:
@app.route('/register_machine', methods=['POST'])
def register_machine():

    data = request.get_json()

    id = data['id']
    name = data['name']

    new_machine = {
        'id': id,
        'name': name,
    }

    machine.append(new_machine)
    
    return jsonify({'machine':machine})

#2.Report an issue:
@app.route('/report_issue', methods=['POST'])
def report_issue():

    data = request.get_json()

    machine_id = data['machine_id']
    issue = data['issue']
    description = data['description']

    report = {
        'machine_id':machine_id,
        'issue':issue,
        'description':description
    }
    
    return jsonify({'report':report})

#3.Retrive all issue reports:
@app.route('/all_report_issue', methods=['POST'])
def all_report_issue():

    data = request.get_json()

    id = data['id']
    machine_id = data['machine_id']
    issue = data['issue']
    description = data['description']
    timestamp = data['timestamp']
    status = data['status']
    
    report = []
    for i in range(len(machine_id)):
        add_report = {
                        'id':id[i],
                        'machine_id':machine_id[i],
                        'issue':issue[i],
                        'description':description[i],
                        'timestamp':timestamp[i],
                        'status':status[i],
                    }
        report.append(add_report)
    
    return jsonify({'reports':report})

#4.Filter issue reports:
@app.route('/report_machine', methods=['POST'])
def report_machine():

    data = request.get_json()

    id = data['id']
    machine_id = data['machine_id']
    issue = data['issue']
    description = data['description']
    timestamp = data['timestamp']
    status = data['status']
    
    report = []
    for i in range(len(machine_id)):
        add_report = {
                        'id':id[i],
                        'machine_id':machine_id[i],
                        'issue':issue[i],
                        'description':description[i],
                        'timestamp':timestamp[i],
                        'status':status[i],
                    }
        report.append(add_report)
    
    filtered_machine_id = [item for item in report if item['machine_id'] == max(data['machine_id'])]
    print(filtered_machine_id[0])

    filter_status = ['Open','Resolved','Urgent']
    filtered_status = [item for item in report if item['status'] in filter_status]
    print(filtered_status[0])
    
    return jsonify({'reports':filtered_machine_id[0]})

#5.API for Counting Issue Reports Per Machine:
@app.route('/count_issue_machine', methods=['POST'])
def count_issue_machine():

    data = request.get_json()
    machine_id = data['machine_id']

    cnt = {}
    for i in machine_id:
        cnt[i] = machine_id.count(i)
    cnt_key = list(cnt.keys())
    
    report = []
    for i in range(0, len(cnt)):
        print(cnt_key[i])
        add_report = {
                        'machine_id':cnt_key[i],
                        'issue_count':cnt[cnt_key[i]],
                    }
        report.append(add_report)
    
    return jsonify({'reports':report})

#6.Count Common Words Across All Issue Titles and Descriptions with Dynamically Specified Top K:
@app.route('/count_comm_words', methods=['POST'])
def count_comm_words():

    nltk.download('stopwords')
    stop_word = stopwords.words('english')

    data = request.get_json()
    description = data['description']

    def get_top_k_common_words(issues, top_k=5):
        description = issues
        data_1 = []
        for val in description:
            val_2 = val.split()
            for n in val_2:
                if (str(n) not in stop_word) and (str(n) not in ['The']):
                    data_1.append(n)

        cnt = {}
        for i in data_1:
            cnt[i] = data_1.count(i)
        cnt_key = list(cnt.keys())

        report = []
        for i in range(top_k):
            add_report = {
                        "word": cnt_key[i], 
                        "frequency": cnt[cnt_key[i]],
                    }
            report.append(add_report)
        
        return report

    report_2 = get_top_k_common_words(description, top_k=2)
    report_5 = get_top_k_common_words(description, top_k=5)

    return jsonify({'reports top 2':report_2, 'reports top 5':report_5 })

if __name__ == '__main__':
    app.run(debug = True)


