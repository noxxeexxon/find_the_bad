import xmltodict
import json
import hashlib
import time
from data_managers.writers.elasticsearch_writer import ElasticsearchWriter
from helpers.maxmind.maxmind_enhance import Maxmind

def get_log_id(log):
    # Generate a unique id for the provided log
    hasher = hashlib.blake2b(digest_size=20)
    hasher.update(log)
    return hasher.hexdigest()

def get_bulk_prepped_log(data_id, log, base_index='eventlogs', log_type='eventlog'):
        # Format the log to get it ready for bulk insert
        index_name = "{}".format(base_index)
        # Some cleaning
        log['System']['EventID'] = str(log['System']['EventID'])
        log['_index'] = index_name
        log['_type'] = log_type
        log['_id'] = data_id
        return log

def parse_log(es_writer, file_path='data/the_bad.xml', initialize=True):
    # Loads the local log file, does geo enchancement and then puts it into ES
    print('Starting parse log process')
    maxmind_lookup = Maxmind()
    print('Opening log file and reading')
    log_file = open(file_path).read()
    parse_result = xmltodict.parse(log_file)
    processed_logs = []
    print('Loading logs into ES')
    for row in parse_result['Events']['Event']:
        event_data = {}
        #print(json.dumps(row, sort_keys=True, indent=2))
        for item in row['EventData']['Data']:
            if '@Name' in item and '#text' in item:
                event_data[item['@Name']] = item['#text']
        
        if 'DestinationIp' in event_data:
            destination_ip_info = maxmind_lookup.get_maxmind_info(event_data['DestinationIp'])
            event_data['DestinationIpInfo'] = destination_ip_info
            if destination_ip_info['geo']['country'] not in ['Unknown', 'United States', 'Hong Kong']:
                continue
        if 'SourceIp' in event_data:
            source_ip_info = maxmind_lookup.get_maxmind_info(event_data['SourceIp'])
            event_data['SourceIpInfo'] = source_ip_info
        row['EventData']['Data'] = event_data
        print('Inserting log')
        # Code for inserting single logs
        #es_writer.insert_log(
        #    'eventlogs'
        #    get_log_id(json.dumps(row).encode('utf-8')),
        #    row
        )
        processed_logs.append(
            get_bulk_prepped_log(
                get_log_id(json.dumps(row).encode('utf-8')),
                row
            )
        )
    es_writer.bulk_insert(processed_logs)
    print('Done')

if __name__ == "__main__":
    es_connected = False
    es_writer = None
    # Dirty hack to deal with this container not starting first 
    # And if the ES connection doesn't work
    while not es_connected:
        try:
            es_writer = ElasticsearchWriter(initialize=True)
            es_connected = True
        except Exception as ex:
            print('Failed to connect sleeping for 5 -> {0}'.format(ex))
            time.sleep(5)
            continue
    parse_log(es_writer)
