# Code for "TSM: Temporal Shift Module for Efficient Video Understanding"
# arXiv:1811.08383
# Ji Lin*, Chuang Gan, Song Han
# {jilin, songhan}@mit.edu, ganchuang@csail.mit.edu
# ------------------------------------------------------
# Code adapted from https://github.com/metalbubble/TRN-pytorch/blob/master/process_dataset.py

import os


dataset_train_path = '/export/sdb/home/lizhenyang8/data/kinetics-400/compress/train_256_frames/'
dataset_val_path = '/export/sdb/home/lizhenyang8/data/kinetics-400/compress/val_256_frames/'
#dataset_frame_path = [dataset_val_path, dataset_train_path]
dataset_frame_path = [dataset_val_path]
label_path = '/export/sdb/home/lizhenyang8/data/kinetics-400/label'

if __name__ == '__main__':
    with open('kinetics_label_map.txt') as f:
        categories = f.readlines()
        #categories = [c.strip().replace(' ', '_').replace('"', '').replace('(', '').replace(')', '').replace("'", '') for c in categories]
        categories = [c.strip().replace(' ', '_').replace('"', '') for c in categories]
    assert len(set(categories)) == 400
    dict_categories = {}
    for i, category in enumerate(categories):
        dict_categories[category] = i

    print(dict_categories)

    #files_input = ['kinetics_val.csv', 'kinetics_train.csv']
    files_input = ['kinetics-400_val.csv'] #'kinetics-400_train.csv' 'kinetics-400_val.csv'
    files_output = ['val_videofolder.txt'] #'train_videofolder.txt' 'val_videofolder.txt'
    for (filename_input, filename_output, dataset_path) in zip(files_input, files_output, dataset_frame_path):
        count_cat = {k: 0 for k in dict_categories.keys()}
        with open(os.path.join(label_path, filename_input)) as f:
            lines = f.readlines()[1:]
        folders = []
        idx_categories = []
        categories_list = []
        for line in lines:
            line = line.rstrip()
            items = line.split(',')
            #folders.append(items[1] + '_' + items[2])
            # for trainset
            #folders.append( "%s_%06d_%06d" % (items[1], int(items[2]), int(items[3])) )
            # for valset
            folders.append( "%s" % (items[1],) )
            #this_catergory = items[0].replace(' ', '_').replace('"', '').replace('(', '').replace(')', '').replace("'", '')
            this_catergory = items[0].replace(' ', '_').replace('"', '')
            categories_list.append(this_catergory)
            idx_categories.append(dict_categories[this_catergory])
            count_cat[this_catergory] += 1
        print(max(count_cat.values()))

        assert len(idx_categories) == len(folders)
        missing_folders = []
        output = []
        for i in range(len(folders)):
            curFolder = folders[i]
            curIDX = idx_categories[i]
            # counting the number of frames in each video folders
            img_dir = os.path.join(dataset_path, categories_list[i], curFolder)
            if not os.path.exists(img_dir):
                missing_folders.append(img_dir)
                # print(missing_folders)
            else:
                dir_files = os.listdir(img_dir)
                output.append('%s %d %d'%(os.path.join(categories_list[i], curFolder), len(dir_files), curIDX))
            print('%d/%d, missing %d'%(i, len(folders), len(missing_folders)))
        with open(os.path.join(label_path, filename_output),'w') as f:
            f.write('\n'.join(output)+'\n')
        with open(os.path.join(label_path, 'missing_' + filename_output),'w') as f:
            f.write('\n'.join(missing_folders)+'\n')
