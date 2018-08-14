#!/usr/bin/env python
import argparse
import json
import os
import subprocess


class BuildDeploy:

    def __init__(self):
        self.MODES = ['base', 'local', 'dev', 'production']
        self.PIPENV = 'pipenv lock --requirements '
        self.PIPENV_DEV = self.PIPENV + ' --dev '

        self.REQUIREMENTS = '> requirements.txt'

    # pipenv lock으로 requirements.txt 생성
    def make_requirements(self, mode):
        if mode == 'dev':
            return subprocess.call(self.PIPENV_DEV + self.REQUIREMENTS, shell=True)
        return subprocess.call(self.PIPENV + self.REQUIREMENTS, shell=True)

    # docker build
    def build_docker(self, mode):
        try:
            for item in self.MODES:
                if mode == item:
                    subprocess.call(f'docker build -t fc-project:{mode} -f Dockerfile.{mode} .', shell=True)
        finally:
            os.remove('requirements.txt')

    def get_mode(self):
        # ./build.py --mode <mode>
        # ./build.py -m <mode>
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-m', '--mode',
            help='Docker build mode [{}]'.format(', '.join(self.MODES)),
        )
        args = parser.parse_args()

        # 모듈 호출에 옵션으로 mode를 전달한 경우
        if args.mode:
            mode = args.mode.strip().lower()
        # 사용자 입력으로 mode를 선택한 경우
        else:
            while True:
                print('Select mode')
                for i, mode_name in enumerate(self.MODES, start=1):
                    print(f' {i}. {mode_name}')
                selected_mode = input('Choice: ')
                try:
                    mode_index = int(selected_mode) - 1
                    mode = self.MODES[mode_index]
                    break
                except IndexError:
                    print('1 ~ 2번을 입력하세요')
        return mode

    def mode_function(self, mode):
        if mode in self.MODES:
            self.make_requirements(mode)
            self.build_docker(mode)
        else:
            raise ValueError(f'{self.MODES}에 속하는 모드만 가능합니다.')


class ResetDatabase:
    def __init__(self):
        self.secrets = json.load(open(os.path.join('.secrets', 'secrets.json')))

    def drop_rds_database(self):
        drop_db = f"PGPASSWORD={self.secrets['DATABASES']['default']['PASSWORD']} psql "
        drop_db += f"--host={self.secrets['DATABASES']['default']['HOST']} "
        drop_db += f"--user={self.secrets['DATABASES']['default']['USER']} "
        drop_db += f"--port={self.secrets['DATABASES']['default']['PORT']} "
        drop_db += f"postgres -c 'DROP DATABASE {self.secrets['DATABASES']['default']['NAME']};'"

        cmd = subprocess.call(
            drop_db,
            shell=True,
        )
        return cmd

    def create_rds_database(self):
        create_db = f"PGPASSWORD={self.secrets['DATABASES']['default']['PASSWORD']} psql "
        create_db += f"--host={self.secrets['DATABASES']['default']['HOST']} "
        create_db += f"--user={self.secrets['DATABASES']['default']['USER']} "
        create_db += f"--port={self.secrets['DATABASES']['default']['PORT']} "
        create_db += f"postgres -c 'CREATE DATABASE {self.secrets['DATABASES']['default']['NAME']} "
        create_db += f"OWNER {self.secrets['DATABASES']['default']['USER']};'"

        cmd = subprocess.call(
            create_db,
            shell=True,
        )
        return cmd


class ChooseMode:
    def __init__(self):
        self.CHOICE = ['Reset Database', 'Build Deploy']

    def get_index(self):
        while True:
            print('Select choice')
            for i, choice in enumerate(self.CHOICE, start=1):
                print(f' {i}. {choice}')
            selected_choice = input('Choice: ')
            try:
                choice_index = int(selected_choice) - 1
                index = self.CHOICE[choice_index]
                break
            except IndexError:
                print('다시 입력해주세요.')
        return index

    def index_function(self, index):
        if index == 'Reset Database':
            reset_db = ResetDatabase()
            reset_db.drop_rds_database()
            reset_db.create_rds_database()
        elif index == 'Build Deploy':
            mode_choice = BuildDeploy()
            mode = mode_choice.get_mode()
            BuildDeploy.mode_function(mode_choice, mode)
        else:
            raise ValueError(f'{self.CHOICE}에 속하는 선택만 가능합니다.')


if __name__ == '__main__':
    run = ChooseMode()
    index = run.get_index()
    ChooseMode.index_function(run, index)