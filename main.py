import datetime

from dotenv import load_dotenv

from ai_daily import make_graph_memory

load_dotenv()

if __name__ == '__main__':
    app = make_graph_memory()
    config = {"configurable": {"thread_id": str(datetime.datetime.today()), 'audio': True}}
    for event in app.stream({'dialogue': []}, config, stream_mode="updates"):
        for node_name, value in event.items():
            if value and 'dialogue' in value:
                print('-' * 100)
                print(node_name)
                print('\n'.join(value['dialogue']))
    print('-' * 100)

