from core.config import settings

if __name__ == "__main__":
    import agent
    import pandas as pd
    from dotenv import dotenv_values
    from datetime import datetime

    try:
        df = pd.read_csv(f'./result_{settings.MODEL_PATH.split("/")[-1].split(".")[0]}.csv', index_col="Unnamed: 0")
    except FileNotFoundError:
        df = pd.DataFrame()

    tokens_config = eval(dotenv_values("tokens.env")[settings.MODEL_TYPE])

    with open("user_messages.txt", "r", encoding='UTF-8') as file:
        messages = [line.rstrip() for line in file]

    result = {}

    for i, user_message in enumerate(messages):
        start_time = datetime.now()

        input_dict = {
            "first_token": tokens_config.get("first_token", None),
            "start_header": tokens_config.get("start_header", None),
            "end_header": tokens_config.get("end_header", None),
            "end_message": tokens_config.get("end_message", None),
            "user_message": user_message
        }
        post = agent.local_agent.invoke(input_dict)
        post["time"] = datetime.now() - start_time
        for key in post.keys():
            result[key] = result.get(key, []) + [post[key]]

    post_df = pd.DataFrame.from_dict(result)
    post_df['model'] = settings.MODEL_PATH.split("/")[-1]
    df = pd.concat([df, post_df], axis=0)

    df.to_csv(f'./result_{settings.MODEL_PATH.split("/")[-1].split(".")[0]}.csv')
