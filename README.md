# gpt_server

本项目依托fastchat的基础能力来提供**openai server**的能力.
1. **在此基础上完美适配了更多的模型**，**优化了fastchat兼容较差的模型**
2. 重新适配了vllm对模型适配较差，导致解码内容和hf不对齐的问题。
3. 支持了**vllm**和**hf**的加载方式
4. 支持所有兼容sentence_transformers的语义向量模型（Embedding和Reranker）
5. Chat模板支持了**function**角色，使其完美支持了**LangGraph Agent**框架
6. **降低了模型适配的难度和项目使用的难度**(仅需适配10行以内的相似代码)，从而更容易的部署自己最新的模型。

（仓库初步构建中，构建过程中没有经过完善的回归测试，可能会发生已适配的模型不可用的Bug,欢迎提出改进或者适配模型的建议意见。）

## 更新信息

```plaintext
4-20  支持了 llama-3
4-13  支持了 deepseek
4-4   支持了 embedding模型 acge_text_embedding (通过测试)
3-9   支持了 reranker 模型 （ bge-reranker，bce-reranker-base_v1）
3-3   支持了 internlm-1.0 ,internlm-2.0
3-2   支持了 qwen-2 0.5B, 1.8B, 4B, 7B, 14B, and 72B
2-4   支持了 vllm 实现
1-6   支持了 Yi-34B
12-31 支持了 qwen-7b, qwen-14b
12-30 支持了 all-embedding(理论上支持所有的词嵌入模型)
12-24 支持了 chatglm3-6b 
```

## 支持的模型


| Models                  | HF | vllm |
| ---------------------- | -- | ---- |
| chatglm3-6b             | √ | √   |
| Qwen (7B, 14B, etc.)) | √ | √   |
| Qwen-2 (0.5B--72B) | √   |   √   |
| Yi-34B                 | √ | √   |
| Internlm-1.0                 | √ | √   |
| Internlm-2.0                 | √ | √   |
| Deepseek                 | √ | √   |
| Llama-3                 | √ | -   |

-----

<br>

**原则上支持所有的Embedding/Rerank 模型**
<br>
以下模型经过测试：
| Embedding/Rerank  | HF |
|----|---|
|bge-reranker|√|
|bce-reranker|√|
|bge-embedding|√|
|bce-embedding|√|
|piccolo-base-zh-embedding|√|
|acge_text_embedding|√| 


目前 **acge_text_embedding** MTEB榜单排行第一, 超越付费的闭源服务，阿里云OpenSearch服务(第二)和baichuan-text-embedding(第五)

## 启用方式

### Python启动

#### 1. 修改配置文件

[config.yaml](https://github.com/shell-nlp/gpt_server/blob/main/gpt_server/script/config.yaml "配置文件")

```bash
cd gpt_server/script
vim config.yaml
```

```yaml
serve_args:
  host: 0.0.0.0
  port: 8082

models:
  - chatglm3-6b:  # 自定义的模型名称
      alias: gpt4,gpt3 # 模型别名     例如  gpt4,gpt3
      enable: false  # 是否启动这个模型   false / true
      model_name_or_path: /home/dev/model/chatglm3-6b/  # 模型的路径
      model_type: chatglm3  # 模型的类型 现在暂时 只有 chatglm3  embedding
      work_mode: hf # 启动方式  vllm  hf
      device: gpu  # gpu / cpu
      workers: 
      - gpus: # 第一个 worker 每一个 -gpus 表示一个 worker
        - 1  # 每个worker 使用的gpu
        - 2
        # - 3
      # - gpus:   # 第二个 worker
      #   - 1

  # Embedding 模型 同上
  - piccolo-base-zh:
      alias: null # 别名   
      enable: true  # false true
      model_name_or_path: /home/dev/model/assets/embeddings/sensenova/piccolo-base-zh/
      model_type: embedding
      work_mode: hf
      device: gpu  # gpu / cpu
      workers:
      - gpus:
        - 0

```

#### 2. 运行命令

[start.sh](https://github.com/shell-nlp/gpt_server/blob/main/gpt_server/script/start.sh "服务主文件")

```bash
sh start.sh
```

### Docker安装
待填充

### 3. 使用 openai 库 进行调用

**见 gpt_server/tests 目录 样例测试代码**
<br>
https://github.com/shell-nlp/gpt_server/tree/main/tests

## 致谢

    FastChat :  https://github.com/lm-sys/FastChat

    vllm :  https://github.com/vllm-project/vllm

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=shell-nlp/gpt_server&type=Date)](https://star-history.com/#shell-nlp/gpt_server&Date)
