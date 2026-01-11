from paddleocr import PaddleOCRVL
import glob

# 英伟达 GPU
pipeline = PaddleOCRVL()
# 昆仑芯 XPU
# pipeline = PaddleOCRVL(device="xpu")
# 海光 DCU
# pipeline = PaddleOCRVL(device="dcu")
# 沐曦 GPU
# pipeline = PaddleOCRVL(device="metax_gpu")

# pipeline = PaddleOCRVL(use_doc_orientation_classify=True) # 通过 use_doc_orientation_classify 指定是否使用文档方向分类模型
# pipeline = PaddleOCRVL(use_doc_unwarping=True) # 通过 use_doc_unwarping 指定是否使用文本图像矫正模块
# pipeline = PaddleOCRVL(use_layout_detection=False) # 通过 use_layout_detection 指定是否使用版面区域检测排序模块

for i in range(10, 7670, 10):
    # result = pipeline.predict("./screenshot1.png")
    # result = pipeline.predict("./xx.jpg")
    filename = f"./screenshot{i}.png"
    print(filename)
    result = pipeline.predict(filename)
    # i = 0
    for res in result:
        # i += 1
        # print("xx"+str(i))
        print(res.markdown['markdown_texts'])
        # print(res['content'])

# for res in output:
#     res.print() ## 打印预测的结构化输出
#     res.save_to_json(save_path="output") ## 保存当前图像的结构化json结果
#     res.save_to_markdown(save_path="output") ## 保存当前图像的markdown格式的结果
