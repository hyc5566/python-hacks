

def test_function():
    """_summary_
        - try 區塊若有錯誤，則執行 except 區塊; 若無錯誤，則執行 else 區塊. 最後執行 finally 區塊.
        - 在 except 及 else 區塊中, 若有 return 返回值, 在 return 前會執行 finally 區塊.
        - 若 finally 區塊有 return 返回值, 則此返回值會蓋過 except 及 else 區塊的返回值.
          資源釋放保證: 這就是為什麼 finally 通常用於確保資源釋放（如關閉檔案、資料庫連接等），無論函數如何結束。
    """    
    try:
        print("執行 try 區塊")
        # assert False
    except Exception:
        print("執行 except 區塊")
        return "except 返回值"
    else:
        print("執行 else 區塊")
        return "else 返回值"
    finally:
        print("執行 finally 區塊")
        # return "finally 返回值"
    
print(f"函數返回值: {test_function()}")
