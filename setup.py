from setuptools import setup

setup(name='Lerner',
      version='0.1',
      description='Streaming desktop notifications from the web',
      author='Zhehao Mao',
      author_email='zhehao.mao@gmail.com',
      url='https://github.com/zhemao/lerner',
      scripts=['lerner'],
      dependencies=['redis', 'PyGObject']
      )
