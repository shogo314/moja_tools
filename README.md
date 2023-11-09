# moja_tools
MojaCoderに関する作問補助ツール。

# インストール
```
pip install git+https://github.com/shogo314/moja_tools.git
```

# 使い方

## rime_to_zip
[Rime](https://github.com/icpc-jag/rime)で管理された問題をMojaCoderに投稿できる`zip`にする。

[https://github.com/shogo314/moja]で実際に使っているので参考にしてください。

```
rime test
```
を実行したあとの状態で下を実行する。

```
mjtools rime_to_zip <problem_dir_name>
```

問題Slugはディレクトリの名前
