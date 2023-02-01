import yaml
import json
import fnmatch
import os

def write_json(path, json_data):
    with open(path, 'w') as file_out:
        json.dump(json_data, file_out)


def read_json(path):
    with open(path) as file_in:
        return json.load(file_in)
    
def modify_yaml(media_path):
    #media_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    
    
    #hardcode path
    path = os.path.abspath("../peeking-duck/pipeline_config.yml")
    with open(path) as f:
        pipeline = yaml.safe_load(f)
        node = pipeline['nodes']
        visual = node[0]['input.visual']
        visual['source'] = media_path
        
    with open(path, 'w') as f:
        yaml.dump(pipeline, f)
        
    
def retrieve_pred_filename(filename,pred_path):
    filename_wo_ext, ext = filename.rsplit('.')
    pattern = filename_wo_ext + '_*.' + ext

    for pred_filename in os.listdir(pred_path):
        print(pred_filename,pattern)
        if fnmatch.fnmatch(pred_filename,pattern):
            return pred_filename
    raise ValueError('File Unlocated')