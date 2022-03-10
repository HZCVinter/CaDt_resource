
class RSA:
    def __init__(self):
        pass

    # 生成质数
    @staticmethod
    def prime_num(range_start, range_stop):
        """
        埃拉托色尼筛选法:
        （1）先把1删除（现今数学界1既不是质数也不是合数）
        （2）读取队列中当前最小的数2，然后把2的倍数删去
        （3）读取队列中当前最小的数3，然后把3的倍数删去
        （4）读取队列中当前最小的数5，然后把5的倍数删去
        （5）读取队列中当前最小的数7，然后把7的倍数删去
        （6）如上所述直到需求的范围内所有的数均删除或读取
        注：此处的队列并非数据结构队列，如需保留运算结果，出于存储空间的充分利用以及大量删除操作的实施，建议采用链表的数据结构
        """
        res_list = []
        for i in range(range_start, range_stop):
            if i <= 1:
                continue
            tem = map(lambda x: x[0] % x[1], zip([i] * 4, [2, 3, 5, 7]))
            if i in [2, 3, 5, 7]:
                res_list.append(i)
            else:
                if 0 not in tem:
                    res_list.append(i)
        return res_list

    # 根据p、q和e生成公钥和私钥
    @staticmethod
    def generate_key(p, q, e, beishu=2):
        t = (p - 1) * (q - 1)
        n = p * q
        d = None
        if 1 < e < t and t % e != 0:
            for i in range(1, t * beishu + 1):
                if (i * e) % t == 1:
                    d = i
                    break
            if d is None:
                raise ValueError
        else:
            print("e_range有误，不符合1 < e < (p-1)*(q-1)，或e是(p-1)*(q-1)的因数")
            raise KeyError
        return [(e, n), (d, n)]

    # 根据p、q和范围e生成公钥和私钥
    @staticmethod
    def generate_key_range(p, q, e_range):
        from tqdm import trange
        res_key = None
        for i in trange(*e_range):
            try:
                res = RSA.generate_key(p, q, i)
                if res[1][0] is not None:
                    res_key = res
                    break
            except Exception:
                pass
        if res_key is None:
            raise ValueError
        else:
            return res_key

    # 获取n允许的最小值
    @staticmethod
    def gene_min_n(strs):
        ord_list = []
        for i in strs:
            ord_list.append(ord(i))
        return max(ord_list) + 1

    # 根据公钥加密字符串
    @staticmethod
    def public_key_encrypt(strs, public_key):
        if len(public_key) != 2:
            print("公钥必须输入长度为2的数组或列表")
            raise KeyError
        ord_list = []
        ciphertext = []
        for i in strs:
            ord_list.append(ord(i))
        for i in ord_list:
            ciphertext.append((i ** public_key[0]) % public_key[1])
        return ciphertext

    # 根据私钥解密字符串
    @staticmethod
    def private_key_decrypt(ciphertext, private_key):
        ord_list = []
        res_list = []
        for i in ciphertext:
            ord_list.append((i ** private_key[0]) % private_key[1])
        for i in ord_list:
            res_list.append(chr(i))
        return "".join(res_list)




if __name__ == '__main__':
    # print("N最小值: ", RSA.gene_min_n("caonima"))
    # print("公钥和私钥: ", RSA.generate_key_range(179, 199, (1000, 2000)))
    print("密文: ", RSA.public_key_encrypt("caonima", (1003, 35621)))
    print("解密: ", RSA.private_key_decrypt([205, 11213, 34853, 29402, 25203, 7617, 11213], (12931, 35621)))




