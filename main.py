from multiprocessing import Process
import os

from generate_tweets import gen_tweets


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(user_one, user_two):
    args = dict()
    args['nsamples'] = 1
    args['length'] = 1023
    args['prefix'] = None
    args['truncate'] = None
    args['batch_size'] = 1
    args['include_prefix'] = True
    args['models_dir'] = "./models"
    args['checkpoint_dir'] = "./checkpoint"
    args['destination_path'] = None
    args['seed'] = None
    args['top_p'] = 0.0
    args['top_k'] = 40
    args['temperature'] = 1
    args['return_as_list'] = True
    args['model_name']= '124M'
    args['run_name'] = f'{user_one}_{user_two}_v2'

    gen_tweets(args)

    info("main_process")


def main(user_1, user_2):
    print(f"user_1 from main.py {user_1}")
    print(f"user_2 from main.py {user_2}")
    info('main line')
    p = Process(target = f, args=(user_1, user_2))
    p.start()
    p.join()

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=("annakhachiyan", "FINALLEVEL"))
#     p.start()
#     p.join()
#
#
