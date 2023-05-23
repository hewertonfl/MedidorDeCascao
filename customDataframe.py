import pandas as pd

flag = 0


def create_dataframe(x=None, y=None):
    global flag
    if not flag:
        data = []
        df = pd.DataFrame(
            data, columns=["Diâmetro [mm]", "Tempo [s]"], dtype=str)
        df.to_csv('./assets/medicao.csv', index=False)
        flag = True
    if not x:
        return
    else:
        df = pd.read_csv('./assets/medicao.csv')
        df.loc[-1] = [y, str(x)]
        df.to_csv('./assets/medicao.csv', index=False)
