from multiprocessing import Pool, cpu_count
import time

def factorize(*number):
    res = []
    for num in number:
        result = []
        for i in range(1, num+1):
            if num%i == 0:
                #print(result)
                result.append(i)

        #print(result)
        res.append(result)
    return res

if __name__ == '__main__':
    print('pool')
    start_with_pool = time.time()
    with Pool(processes=cpu_count()) as pool:
        poll_result = pool.map(factorize, [128, 255, 99999, 10651060])
        result = [i[0] for i in poll_result]
        a, b, c, d = result
        assert a == [1, 2, 4, 8, 16, 32, 64, 128]
        assert b == [1, 3, 5, 15, 17, 51, 85, 255]
        assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
        assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                     1521580, 2130212, 2662765, 5325530, 10651060]
    print(time.time()-start_with_pool)
    print()
    print('single')
    start = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    print(time.time() - start)
