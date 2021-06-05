from os import path

COL_NAMES = ['0.precision', '0.recall', '0.f1-score', '0.support',
             '1.precision', '1.recall', '1.f1-score', '1.support',
             '2.precision', '2.recall', '2.f1-score', '2.support',
             'accuracy',
             'macro avg.precision', 'macro avg.recall', 'macro avg.f1-score', 'macro avg.support',
             'weighted avg.precision', 'weighted avg.recall', 'weighted avg.f1-score', 'weighted avg.support']


def create_file(file_path):
    header = '\t'.join(COL_NAMES) + '\n'

    with open(file_path, 'w+') as f:
        f.write(header)


def dict_to_csv(dict_metrics, file_path):
    # if file does not exist create it and write header
    if not path.exists(file_path):
        create_file(file_path)

    with open(file_path, 'a+') as f:
        values = []
        for col_name in COL_NAMES:
            path_segments = col_name.split('.')
            value = dict_metrics
            for path_segment in path_segments:
                value = value[path_segment]
            values.append(str(value))
        f.write('\t'.join(values) + '\n')


if __name__ == '__main__':
    json = {'0': {'precision': 0.8040816326530612, 'recall': 0.5549295774647888, 'f1-score': 0.6566666666666666, 'support': 355}, '1': {'precision': 0.3645833333333333, 'recall': 0.6829268292682927, 'f1-score': 0.47538200339558573, 'support': 205}, '2': {'precision': 0.831275720164609, 'recall': 0.7279279279279279, 'f1-score': 0.7761767531219981, 'support': 555}, 'accuracy': 0.6645739910313901, 'macro avg': {'precision': 0.6666468953836678, 'recall': 0.6552614448870031, 'f1-score': 0.6360751410614168, 'support': 1115}, 'weighted avg': {'precision': 0.7368130830641507, 'recall': 0.6645739910313901, 'f1-score': 0.6828233859600633, 'support': 1115}}
    dict_to_csv(json, 'test22111d.csv')