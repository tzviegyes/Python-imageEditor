import image_editor as ie

def test_separate_channels():
    combined_image = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]], [[13, 14, 15], [16, 17, 18]]]
    seperated_image = [[[1, 4], [7, 10], [13, 16]], [[2, 5], [8, 11], [14, 17]], [[3, 6], [9, 12], [15, 18]]]
    combined_image_2 = [[[1, 2], [4, 5]], [[7, 8], [10, 11]], [[13, 14], [16, 17]]]
    seperated_image_2 = [[[1, 4], [7, 10], [13, 16]], [[2, 5], [8, 11], [14, 17]]]
    wrong_seperated_image = [[[1, 4], [7, 10], [13, 16]], [[2, 5], [8, 11], [14, 17]], [[3, 6], [9, 12], [15, 1]]]

    assert ie.separate_channels(combined_image) == seperated_image
    assert ie.separate_channels(combined_image_2) == seperated_image_2
    assert ie.separate_channels(combined_image) != wrong_seperated_image

def test_combine_channels():
    input_1 = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]
    output_1 = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    input_2 = [[[1, 4], [7, 10], [13, 16]], [[2, 5], [8, 11], [14, 17]], [[3, 6], [9, 12], [15, 18]]]
    output_2 = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]], [[13, 14, 15], [16, 17, 18]]]
    assert ie.combine_channels(input_1) == output_1
    assert ie.combine_channels(input_2) == output_2

def test_RGB2grayscale():
    assert ie.RGB2grayscale([[[100, 180, 240]]]) == [[163]]
    assert ie.RGB2grayscale([[[200, 0, 14], [15, 6, 50]]]) == [[61, 14]]

def test_blur_kernel():
    assert ie.blur_kernel(3) == [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    assert ie.blur_kernel(1) == [[1]]

def test_apply_kernal():
    assert ie.apply_kernel([[0, 128, 255]], ie.blur_kernel(3)) == [[14, 128, 241]]
    input_image = [[10, 20, 30, 40, 50], [8, 16, 24, 32, 40], [6, 12, 18, 24, 30], [4, 8, 12, 16, 20]]
    output_image = [[12, 20, 26, 34, 44],[11, 17, 22, 27, 34],[10, 16, 20, 24, 29],[7, 11, 16, 18, 21]]
    input_kunal = ie.blur_kernel(5)
    assert ie.apply_kernel(input_image, input_kunal) == output_image

def test_bilinear_interpolation():
    assert ie.bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert ie.bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert ie.bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert ie.bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160
    assert ie.bilinear_interpolation([[15, 30, 45, 60, 75], [90, 105, 120, 135, 150], [165, 180, 195, 210, 225]], 4/5, 8/3) == 115

def test_resize():
    assert ie.resize([[0,64,128],[0, 128, 255],[100, 100, 100]], 2, 2) == [[0,128],[100,100]]
    assert ie.resize([[ 0, 13, 26, 39],[ 52, 65, 78, 91],[104, 117, 130, 143],[156, 169, 182, 195],[208, 221, 234, 247]], 2, 3) == [[0, 20, 39], [208, 228, 247]]

def test_rotate():
    assert ie.rotate_90([[1, 2, 3],[4, 5, 6]], 'R') == [[4, 1], [5, 2], [6, 3]]
    assert ie.rotate_90([[1, 2, 3],[4, 5, 6]], 'L') == [[3, 6], [2, 5], [1, 4]]
    assert ie.rotate_90([[[1, 2, 3], [4, 5, 6]],[[0, 5, 9], [255, 200, 7]]], 'L') == [[[4, 5, 6], [255, 200, 7]], [[1, 2, 3], [0, 5, 9]]]

def test_get_edges():
    assert ie.get_edges([[200, 50, 200]], 3, 3, 10) == [[255, 0, 255]]

def test_quantize():
    assert ie.quantize([[0, 50, 100], [150, 200, 250]], 8) == [[0, 36, 109], [146, 219, 255]]
