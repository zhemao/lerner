from setuptools import setup

setup(name='Notistream',
      version='0.1',
      description='Streaming desktop notifications from the web',
      author='Zhehao Mao',
      author_email='zhehao.mao@gmail.com',
      url='https://github.com/zhemao/notistream',
      scripts=['notistream'],
      dependencies=['redis', 'PyGObject']
      )
