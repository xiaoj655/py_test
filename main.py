import os

if __name__ == '__main__':
    os.system(f"pytest {os.path.join(os.path.dirname(__file__), 'tests/ac_paper.py')} -s")