Expert Systems With Applications 204 (2022) 117372 

**==> picture [61 x 67] intentionally omitted <==**

Contents lists available at ScienceDirect 

## Expert Systems With Applications 

journal homepage: www.elsevier.com/locate/eswa 

**==> picture [61 x 73] intentionally omitted <==**

## Printed label defect detection using twice gradient matching based on improved cosine similarity measure 

**==> picture [29 x 30] intentionally omitted <==**

## Dongming Li[a][,][b] , Jinxing Li[a][,][∗] , Yuanyi Fan[b] , Guangming Lu[a][,][∗] , Jie Ge[a] , Xiaoyang Liu[a] 

a _Department of Computer Science and Technology, Harbin Institute of Technology (Shenzhen), Shenzhen, China_ b _Shenzhen Fugui Precision Industry Co., Ltd., Shenzhen, China_ 

|A R T I C L E|I N F O|A B S T R A C T|
|---|---|---|
|_Keywords:_||Many vision-based methods for printed label defect detection have been proposed to replace inefficient manual|
|Printed label defect|detection|inspection. However, due to the existence of artifacts and noise regions, it usually leads to a large number|
|Gradient matching<br>Artifact<br>Non-rigid local deformation<br>Cosine similarity||of misjudgments. Also, since most of the printed labels are non-rigid, they are prone to local deformation,<br>which will cause lots of artifacts after image subtraction. This paper proposes a novel printed label defect<br>detection framework (PLDD), which performs twice gradient matching based on improved cosine similarity<br>measures. The overall idea is based on comparing a golden master (_𝐺𝑀_) image with test images, thus the|
|||_𝐺𝑀_image is demanded. Specifically, latent defect candidates will be extracted firstly from RGB sub-images|
|||for artifact elimination. Mask mechanism is also introduced to eliminate the influence of background gradient|
|||features around these defect candidates. Experiments compared with existing methods are conducted with|
|||three industrial datasets. The results exhibit that PLDD achieves a high mean _𝐹_1 score (0.9702), and only 103|
|||false positives (_𝐹𝑃_) occurred in 44,628 ground truths. Defects are being detected in real-time with an average|
|||time consuming of 0.26362 s.|



## **1. Introduction** 

Nowadays, manufacturing enterprises in the world are facing increasingly fierce competition, and improving product quality is the key to promoting competitiveness. As the first step of quality control, incoming quality control (IQC) plays a crucial role in preventing defective materials from entering production lines and thus avoiding waste. For a factory, there are thousands of types of printed labels that need to be inspected. Theoretically, any region of a test printed label that is inconsistent with the golden master image can be regarded as a latent defect. The _𝐺𝑀_ image is a defect-free image that is manually selected by an expert. Printing defects contain smudges, duplicates, shifts, scratches, overprints, omissions, and color distortion, etc. Generally, these defects are usually detected manually. However, long-term detection on printing defects by human beings would result in visual fatigue and misjudgment. Therefore, it is necessary to improve the performance and economic efficiency of printing defect detection by computer vision. 

Over the last decade, some traditional approaches have been proposed for printed label defect detection (Shankar et al., 2009; Vans et al., 2011; Zhang et al., 2019). Shankar et al. (2009) first identified regions of interest (ROIs) using edge detection, then performed defect 

detection by using correlation subtraction based on a threshold. Vans et al. (2011) proposed an automatic online visual inspection system for variable data printing derived from structural similarity index measure (SSIM). It is conducted by structural dissimilarity measure. Zhang et al. (2019) utilized a combination of bright and dark templates to overcome image position and illumination deviation. As a result, these approaches reduce the costs of human labor to a certain extent, but few of them pay attention to the negative influence of artifacts. 

Recently, many deep learning-based methods have been innovated to achieve detection. However, even though these methods have gained satisfactory achievements in many natural images, they cannot be directly applied to printed label defect detection. Compared with more than 14 million sample data in the ImageNet (Deng et al., 2009) dataset, the most critical issue in industrial surface defect detection is the number of training samples. Haik et al. (2020) proposed a defect detection for variable data prints with a huge dataset, which contains 20,000 image pairs with 40,000 real defects. However, there are only a few defective images in many real-world industrial scenes. Furthermore, deep learning usually depends on specific types of defects in training, which is quite challenging for unseen detection. Deng et al. (2020) introduced a convolutional neural network (CNN) classifier for 

> ∗ Corresponding author. 

_E-mail addresses:_ 18B953073@stu.hit.edu.cn (D. Li), lijinxing158@hit.edu.cn (J. Li), ian.yy.fan@foxconn.com (Y. Fan), luguangm@hit.edu.cn (G. Lu), 18B953075@stu.hit.edu.cn (J. Ge), 18B953077@stu.hit.edu.cn (X. Liu). 

https://doi.org/10.1016/j.eswa.2022.117372 

Received 30 August 2021; Received in revised form 11 January 2022; Accepted 25 April 2022 Available online 10 May 2022 

0957-4174/© 2022 Elsevier Ltd. All rights reserved. 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [291 x 79] intentionally omitted <==**

**Fig. 1.** Sample artifacts with enhanced visualization by applying a hot colormap. 

defect detection. However, it is challenging to train the classification network with unseen defects. Finally, deep learning is heavily constraint by the GPU requirement, encountering an enormous time cost on training. Valente et al. (2020) presented a semantic segmentation based network to map print defects at a pixel level. However, the main disadvantage is its high computational cost. 

According to this aforementioned analysis, there do exist challenges for automatic printed label defect detection: 

- (1) How to prevent from the inferior influence of artifacts? As most printed labels are made from non-rigid materials, they would easily get irreversible deformation due to the variation of temperature, moisture, and stress. Subsequently, artifacts are created and defect detection is becoming harder. Fig. 1 shows the artifacts by subtracting _𝐺𝑀_ from the test image. 

- (2) How to apply the detection framework to detect an unseen type of defects? There are tens of thousands of categories of printed labels that should be detected. Especially, an unseen type of defect is a general scene in a real-world application. Thus, it is unreasonable to cover all of the categories, and making the detection algorithm enjoy better generalization is a key point. Fig. 2 shows some representative defect samples of printed labels. 

- (3) How to achieve real-time implementation? Obviously, only realtime detection can maximize the efficiency of production lines. Thus, not only accuracy but speed also should be considered simultaneously. 

To tackle these challenges mentioned above, we propose a novel defect detection framework based on traditional machine vision in this paper. We first propose an effective artifact elimination algorithm before defect detection. Then, we utilize the _𝐺𝑀_ and test image to perform twice matching to detect an unseen type of defect with realtime performance. Specifically, twice gradient matching is performed only on latent defect candidates, with an improved cosine similarity measure. 

In summary, our main contributions are summarized as follows: 

- (1) Some artifacts caused by local deformation are eliminated. We propose an effective latent defect candidates extraction (LDCE) algorithm, based on sub-image sliding and RGB channels chromatic aberration. 

- (2) An efficient and credible defect detection algorithm is innovated. Masks are also applied in this algorithm to reduce the influence of unrelated gradient features around defect candidates. Further, a twice matching strategy is also adopted, to detect both missing print and overprint simultaneously. 

- (3) An improved cosine similarity measure is introduced. Motivated by the human visual system, it combines RGB average gradient fusion and nonlinear activation function to fuse the influence of absolute value and direction of the image gradient. 

- (4) Our proposed framework is compared with existing methods, which include SSIM (Wang et al., 2004), real-time print-defect detection system (RTPDS) (Shankar et al., 2009), structural dissimilarity (DSIM) (Vans et al., 2011), FCN-VGG16 (Long et al., 

2015), DeepLabV3+ (Chen et al., 2018), and Valente et al. (2020). Such framework yields encouraging defect detection performance in real-time. And it needs no GPU, which reduces the cost of hardware. 

The remainder of this paper is organized as follows. Section 2 gives a related work description including traditional and deep learning methods. The proposed framework is then analyzed in Section 3. To quantitatively verify the effectiveness of the proposed method, experiments are conducted on real-world datasets in Section 4, followed by the conclusion and future work in Section 5. 

## **2. Related work** 

## _2.1. Methods based on traditional machine vision_ 

Printed matter defect detection based on traditional machine vision has been widely studied (Shankar et al., 2009; Verikas et al., 2011). One popular method is to perform image subtraction (Peng et al., 2010) between a test image and a reference image (without defects) after image alignment, and then the defects are detected through a threshold. However, image subtraction is particularly sensitive to image position and illumination deviation. To tolerate these issues, Zhang et al. (2019) proposed a modified image subtraction method that uses a combination of bright and dark templates to detect printing defects. However, image subtraction does not perform well in the case of local deformation, especially non-rigid deformation. 

Methods based on segmentation and classification are also introduced for printed image quality inspection. Chen et al. (2019) proposed a new segmentation-based framework for local print defects detection. After applying Gaussian pyramids method and selective search method, extracted features are used to classify defects. However, it only focused on gray spot defects on scanned printed pages with consistent texture background, while it cannot fit for other defects types. 

Template matching methods (Bouchot et al., 2011; Tsai et al., 2003; Yangping et al., 2018) have a good generalization on defect detection. The reason is that it focuses on similarity between compared image pairs ( _𝐺𝑀_ and test image), rather than the differences among different types of defects. Ma et al. (2017) proposed a new detection algorithm with twice template matching, which extracts ROIs and distinguishes foreground and background. But its first template matching was based on gray level transformation, thus it was sensitive to illumination deviation and noise. Furthermore, in order to overcome the distortion issue on curved geometry, Gong et al. (2020) introduced a deformable template matching method for transparent label defect detection on a curved glass bottle. Since most template matching methods are performed on every foreground area, heavy calculations are required, and small defects are difficult to be detected. In addition, missing and overprint defects cannot be detected simultaneously by a single template matching process, which is rarely mentioned. 

Besides, similarity measure is conducted in printed matter defect detection. Similarity measure usually includes structural similarity, cosine similarity, etc. Since the artifacts caused by local deformation usually appear near the edge of contours, they are essentially similar 

2 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [407 x 378] intentionally omitted <==**

**Fig. 2.** Some representative defect samples of printed labels. 

to adjacent contours. Therefore, methods based on similarity measure are capable of eliminating these artifacts. In terms of structural similarity, DSIM (Vans et al., 2011) innovated an automatic online visual inspection system for variable data printing (VDP), and took the human visual system into account. DSIM is derived from SSIM and is used to measure the degree of dissimilarity between images. However, DSIM is calculated pixel-by-pixel, which leads to high computational cost, so that it cannot meet real-time requirements. In terms of cosine similarity measure, Asha et al. (2012) proposed similarity-based methods for defect detection on patterned textures. Zhang et al. (2020) proposed an improved cosine similarity measure for fabric defect detection for textile industry. Anyway, the original cosine similarity only considers the direction difference of two vectors, without considering the length difference. This increases the difficulty of defect detection. 

## _2.2. Methods based on deep learning_ 

Since 2012, deep learning methods have achieved remarkable performance in many computer vision tasks, including image classification (Zhang et al., 2021), object detection, and semantic segmentation (Ferguson et al., 2018; Nguyen et al., 2021; Wu et al., 2018). For surface defect detection, methods based on deep learning can be summarized into the following categories: 

- (1) Image classification based networks. In Wu et al. (2017), a CNN feature extraction technique was proposed, working on 

textured images. Deng et al. (2020) proposed a unified defect detection framework comprised of a maximally stable extreme region (MSER) defect candidates generation and a binary CNN classifier. However, the categories of defects of the printed label in the industrial scenario are diverse, even unknown defects types should also be well detected. Therefore, it is a challenging task to prepare training samples for the classification network. 

- (2) Object detection based networks. Haik et al. (2020) proposed a novel approach for inspecting variable data prints (VDP) with an ultra-low false alarm rate (0.005%) and potential applicability to other real-world problems. A dataset containing 20,000 image pairs with 40,000 real defects is collected and labeled for model training to gain high performance. Also, FlowNet2 (Ilg et al., 2017) was used for optical flow computation (registration). However, it is difficult, labor-intensive, and costly to collect and label a large number of high-quality defect images in industries. The same problem exists in previous works such as Di et al. (2019). 

- (3) Autoencoder-based networks. Zhao et al. (2018) combined generative adversarial network (GAN) and autoencoder to propose a defect detection model based on positive sample training without a manual label. Bergmann et al. (2018) pointed out the disadvantages of per-pixel loss functions in autoencoder-based frameworks, and proposed to incorporate spatial information using SSIM to improve segmentation results. But if the background 

3 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

is too complex and random, it is still difficult for autoencoders to reconstruct and repair images. In our printed label defect detection scenario, the text and pattern of a print enjoy great diversity. 

- (4) Semantic segmentation based methods. Yu et al. (2017) presented a novel two-stage fully convolutional network (FCN) framework for surface defect inspection in an industrial environment, and validated the performance on the dataset of DAGM 2007. Tabernik et al. (2020) proposed a segmentation-based deep-learning architecture on a specific domain of surface-crack detection, using only approximately 25–30 defective training samples. However, these methods did not take the reference image into account. Valente et al. (2020) presented the first endto-end framework based on DeepLabV3+ backbone to map print defects at a pixel level, and its framework supports two input modes: Full-Reference (FR) and No-Reference (NR). Anyway, the main disadvantages of semantic segmentation networks are a high computational cost (mainly for large images), and the requirement of a large amount of per-pixel labeled data. 

- (5) Siamese network-based methods. Wu et al. (2019) proposed a siamese network for button surface defect detection, and satisfactory detection results were observed with limited and even imbalanced samples. Luan et al. (2021) applied a siamese network with a defect-sensitive loss function to industrial production defect detection. However, since there are only a few of defective samples, its performance is poor. In addition, once the detection object category changes, these neural networks should be retrained. In industrial applications with variant product categories, frequent re-training could be time-consuming and is not always acceptable. 

To sum up, deep learning method also has various disadvantages and cannot be directly applied to our printed label defect detection scenario. 

## **3. Methodology** 

## _3.1. The proposed framework_ 

Fig. 3 illustrates that the proposed framework consists of two main stages: latent defect candidates extraction and twice gradient matching. In the first stage, to eliminate artifacts caused by local deformation, an effective RGB sub-image sliding process is performed to get a different image. Then, a low-threshold filter is applied to binarize the image. Morphological opening and contour extraction are taken to acquire the final latent defect candidates. The proposed framework then only focuses on latent defect candidates instead of the entire image. Specifically, in the second stage, gradient matching works on each latent defect candidate, and the mask is also combined to extract more discriminative features. Further, a twice matching strategy is adopted to detect both missing print and overprint simultaneously. Moreover, motivated by the human visual system, an improved cosine similarity measure is presented to fuse absolute value and direction of the image gradient through RGB average gradient fusion and non-linear activation function. 

## _3.2. Image registration_ 

The image captured by an industrial camera in real-time inevitably deviates from the _𝐺𝑀_ image, as illustrated in Section 1. Therefore, the test image and _𝐺𝑀_ image should be aligned firstly before the defect detection. In this paper, the image registration is accomplished by shape-based template matching algorithm (Dailin et al., 2013), which could effectively align the test image with the _𝐺𝑀_ image. After the image alignment, median filtering with kernel 3 × 3 is applied to the test and _𝐺𝑀_ image for denoising. 

## _3.3. LDCE algorithm_ 

After the image registration, the differential images should be obtained via image subtraction. However, a large number of artifacts caused by RGB absolute subtraction will increase the difficulty of defect detection. Besides, color images stored by RGB format are uneven, resulting in difficulty to assess the similarity of two colors from their distance in RGB color space (Johnson et al., 2010). Fortunately, color image processing can be invoked in other spaces to exhibit the features of human vision. CIE L*u*v*color space is recommended by the International Commission on Illumination (CIE). It has standardized color space and can reflect the color difference of objects more excellently. However, it is very time-consuming, resulting in difficulty of real-time detection on CPU-only. 

Therefore, a low-cost color difference approximation (Riemersma, 2012) is utilized, and its result is very close to CIE L*u*v*. The detailed formulas are listed as below: 

|_𝛥𝐶_=<br>√<br>(2 +<br>_𝑟_<br>256)⋅_𝛥𝑅_2+ 4⋅_𝛥𝐺_2+ (2 +<br>_𝑟_=<br>_𝐶_1_,𝑅_+_𝐶_2_,𝑅_<br>2<br>_𝛥𝑅_=_𝐶_1_,𝑅_−_𝐶_2_,𝑅_<br>_𝛥𝐺_=_𝐶_1_,𝐺_−_𝐶_2_,𝐺_<br>_𝛥𝐵_=_𝐶_1_,𝐵_−_𝐶_2_,𝐵_|255 −<br>_𝑟_<br>256 ~~)~~⋅_𝛥𝐵_2<br>(1)<br>(2)<br>(3)<br>(4)<br>(5)|
|---|---|



where _𝐶_ 1 _,𝑅_ , _𝐶_ 1 _,𝐺_ , and _𝐶_ 1 _,𝐵_ are the pixel values of R, G, B channels in the image 1, respectively; _𝐶_ 2 _,𝑅_ , _𝐶_ 2 _,𝐺_ , and _𝐶_ 2 _,𝐵_ are the pixel values of R, G, B channels in the image 2, respectively; _𝛥𝐶_ is the color difference. The largest distance of colors should be the distance between black and white, whose pixel gray values are 0 and 255, respectively. However, such largest value calculated by Eq. (1) is 770, which is much larger than 255. Therefore, we propose a revised version in order to keep consistent with gray value. This is defined as follows: 

**==> picture [252 x 19] intentionally omitted <==**

Considering that the minimum pixel value distinguished by human beings is a threshold _𝑇𝑓𝑖𝑙𝑡𝑒𝑟_ , pixels whose values are smaller than _𝑇𝑓𝑖𝑙𝑡𝑒𝑟_ should be ignored in subsequent procedures. Then, a binary threshold is applied to _𝛥𝐶𝑟𝑒𝑣𝑖𝑠𝑒𝑑_ by Eq. (7). 

**==> picture [252 x 25] intentionally omitted <==**

where _𝑑𝑏𝑖𝑛_ is the pixel value of binary image _𝐷𝑏𝑖𝑛_ which includes real defects and artifacts. 

Based on aforementioned analysis, the number of artifacts should be reduced as much as possible via the LDCE algorithm, which is described in Algorithm 1. Here, _𝐺𝑀_ image and test image are split into _𝑛_ × _𝑛_ sub-images with size _𝑤_ × _ℎ_ ; _𝑙_ is the sliding range; _𝑛_ = 2 and _𝑙_ = 5 are set in Section 4. For each sliding window, the sum of sub-image difference ([∑] _𝛥𝐶𝑟𝑒𝑣𝑖𝑠𝑒𝑑_ ) is calculated. The sliding window with the smallest[∑] _𝛥𝐶𝑟𝑒𝑣𝑖𝑠𝑒𝑑_ is chosen for acquiring the best difference image. 

As shown in Fig. 3, the clustered white pixels are the latent defect candidates. Subsequently, the morphological opening operation with a 3 × 3 structure element is applied to the binary image _𝐷𝑏𝑖𝑛_ for denoising. Fig. 4 gives a brief demonstration of the sub-image sliding for artifact elimination and latent defect candidates extraction. The purpose of sub-image sliding is to obtain the best difference image in a certain neighborhood, as well as to eliminate artifacts and extract latent defect candidates. 

4 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [419 x 124] intentionally omitted <==**

**Fig. 3.** Illustration of the proposed framework for printed label defect detection. 

## **Algorithm 1:** LDCE 

**Input:** _𝐺𝑀_ and test ( _𝑇_ ) image, _𝑇𝑓𝑖𝑙𝑡𝑒𝑟, 𝑙, 𝑛, 𝑤, ℎ_ **Output:** All latent defect candidates contained in a set of _𝐶_ **1** Split _𝐺𝑀_ and _𝑇_ image into _𝑛_ × _𝑛_ sub images, _𝐺𝑀_ = { _𝑔𝑚_ 1 _, 𝑔𝑚_ 2 _, ..., 𝑔𝑚𝑛_ × _𝑛_ }, _𝑇_ = { _𝑡_ 1 _, 𝑡_ 2 _, ..., 𝑡𝑛_ × _𝑛_ }, _𝑤_ × _ℎ_ is the width and height of each sub image, _𝐷_ is the differential image, and _𝑆𝑢𝑏𝑘_ is the sub-image of _𝐷_ , _𝑘_ ∈[1 _, 𝑛_ × _𝑛_ ]; 

- **2** _𝑠𝑖,𝑗_ means a sub-image with upper-left coordinate ( _𝑖, 𝑗_ ) and size _𝑤_ × _ℎ_ ; 

- **3 foreach** _sub-image 𝑔𝑚𝑘_ **do** 

- **4** ( _𝑢, 𝑣_ ) is the upper-left coordinate of current _𝑔𝑚𝑘_ ; **5 for** _𝑖𝑖_ ∈[− _𝑙,_ + _𝑙_ ] **do 6 for** _𝑗𝑗_ ∈[− _𝑙,_ + _𝑙_ ] **do 7** calculate[∑] _𝛥𝐶𝑟𝑒𝑣𝑖𝑠𝑒𝑑_ for each _𝑠𝑢_ + _𝑖𝑖,𝑣_ + _𝑗𝑗_ ; **8 end** 

- **9 end** 

- **10** _𝑖, 𝑗_ = argmin _𝑖,𝑗_ ∑ _𝛥𝐶𝑟𝑒𝑣𝑖𝑠𝑒𝑑_ ; **11** copy the corresponding differential result of _𝑠𝑖,𝑗_ to _𝑆𝑢𝑏𝑘_ ; **12 end** 

- **13** _𝐷_ = { _𝑆𝑢𝑏_ 1 _, 𝑆𝑢𝑏_ 2 _, ..., 𝑆𝑢𝑏𝑛_ × _𝑛_ }, apply threshold _𝑇𝑓𝑖𝑙𝑡𝑒𝑟_ for _𝐷_ and get the binary image _𝐷𝑏𝑖𝑛_ ; 

- **14** Perform morphological opening operation to extract contours for _𝐷𝑏𝑖𝑛_ , then output a set _𝐶_ containing all latent defect candidates; 

**==> picture [224 x 116] intentionally omitted <==**

**Fig. 5.** Mask extraction for background feature filtering. 

Then, an absolute subtraction is performed between the test sub-image and _𝐺𝑀_ sub-image, and a threshold filtering is applied to acquire a binary image. In addition, a morphological dilation operation with a 5 × 5 structure element is conducted on the final differential binary image to acquire a dilated image. Finally, a bitwise AND operation is performed to get the final mask, which is utilized in the subsequent defect detection. 

## _3.5. Defect detection_ 

**==> picture [62 x 62] intentionally omitted <==**

**==> picture [63 x 62] intentionally omitted <==**

**==> picture [37 x 35] intentionally omitted <==**

**Fig. 4.** An example of sub-image sliding. Both the _𝐺𝑀_ image and test image are split into several sub-images of the same size. Each sub-image of the _𝐺𝑀_ image is moved in all sliding windows corresponding to the sub-image of the test image. 

## _3.4. Mask extraction for background feature filtering_ 

To eliminate the influence of background gradient features around defect candidates, the mask mechanism is introduced, as illustrated in Fig. 5. Firstly, the contour of the test sub-image is extracted by Canny edge detector, whose thresholds are set to 60 and 130, respectively. 

Despite the fact that most artifacts have been eliminated by the LDCE algorithm, some artifacts are still remaining, especially in large non-rigid deformations. Therefore, it is necessary to seek a discriminative method that can distinguish artifacts and defects. Here, we conduct experiments only on the aforementioned candidates. Compared with methods that detect all regions, the proposed method only detects latent defect candidates resulting in better efficiency, especially on minor defects detection. Generally, each area in a test image should be similar to the corresponding area in the _𝐺𝑀_ image, unless it contains differences, i.e., defects. In this paper, one purpose is to find an efficient similarity assessment method. The subsequent chapter will give a brief analysis concerning the limitation of the cosine similarity measure. 

## _3.5.1. Limitation of cosine similarity measure_ 

The cosine similarity measure is based on the angle between twodimensional vectors. It is known that the angle _𝜃_ between two vectors in plane is defined in Eq. (8). 

**==> picture [251 x 26] intentionally omitted <==**

As the value of cos _𝜃_ ∈[−1 _,_ 1], the cos _𝜃_ can be recognized as the similarity between two vectors. 

5 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [138 x 67] intentionally omitted <==**

**Fig. 6.** Example of cosine similarity comparison. Suppose that image (a) is the test image (the pixel values inside the circle are all 250) and image (b) is the _𝐺𝑀_ image (the pixel values inside the circle are all 150). According to human visual characteristics, image (a) should be considered as a defective image. However, their similarity score of original cosine similarity is 1, and image (a) will be judged as a defect-free image. Fortunately, their similarity score of the improved cosine similarity is 0 and the result is consistent with the human visual characteristics. 

**==> picture [174 x 140] intentionally omitted <==**

**Fig. 7.** Sample detection results of some low-contrast defects. (a): ground truth (marked with yellow bounding boxes). (b): defects detected by gradient fusion of RGB channels (marked with red bounding box). (c): defects that cannot be detected in grayscale images. 

Also, cos _𝜃_ can measure the similarity between two images. Through sobel operator, the gradient information of pixels in _𝑥_ and _𝑦_ direction can be obtained. Thus, gradient information of each pixel can be represented by a two-dimensional array. In each sliding window, the similarity is listed as follows. 

**==> picture [252 x 18] intentionally omitted <==**

where _𝜃_ is the angle between two corresponding vectors. However, the limitation of original cosine similarity is obvious, as it can only evaluate the angle between two vectors without length information. In practice, this means that the difference in image contrast is not fully considered. Fig. 6 illustrates this limitation. We will demonstrate how to improve the original cosine similarity measure in the subsequent chapter. 

## _3.5.2. Improved cosine similarity measure (ICSM)_ 

In general, template matching can be divided into pixel gray value matching and edge-based matching. The normalized cross correlation (NCC) algorithm is the most well-known pixel gray value matching algorithm. However, it is not only sensitively affected by local illumination changes but also computationally expensive. By contrast, edgebased matching is robust against illumination variation with low-cost computation. The idea of edge-based cosine similarity is to calculate the sum of cosine values of angles between gradient vectors of edge points in two images. Here, edge points are obtained by the Canny edge detector. The number of edge points is far less than that of pixels in the entire image, resulting in a significant reduction in the amount of calculation. But cosine similarity is inconsistent with the human visual system in terms of printed label defect detection. To solve this problem, we propose the ICSM approach which is improved as follows: 

- (1) Gradient fusion of RGB channels. For a color image, the general approach is to convert it to a grayscale image before the gradient is extracted. The disadvantage is that certain important gradient information might be missing. Therefore, it results in false detection on some low-contrast defects, whose intensity values are very close to that of the background. To address this problem, the gradients of each RGB channel are fused to acquire more discriminative gradient features. In Fig. 7, the low contrast defects are well detected. 

- (2) Incorporation of the activation function. Inspired by human visual characteristics, a nonlinear activation function is incorporated with the original cosine similarity. As a result, both the length and the direction of image gradient vectors are taken into consideration. The perception of defects in the human visual system depends on the relative brightness of the defects to the background, rather than the absolute brightness. In Fig. 6, there are two different circles in the center of the two images. However, the two images are unreasonably regarded as the same images according to original cosine similarity. This will lead to a large number of false results in real-world printed defect detection. Therefore, we introduce a nonlinear activation function to increase the similarity score of non-defective regions, while suppressing that of defective regions. The experimental results in Section 4 prove that this incorporation is close to human visual characteristics. In addition, the detailed formulas of ICSM are listed from Eqs. (10) to (19). 

**==> picture [252 x 266] intentionally omitted <==**

where _𝑆𝑖𝑚_ ( _𝑇𝑖, 𝐺𝑖_[(] _[𝑢,𝑣]_[)] ) is the similarity score between sub-image _𝑇𝑖_ and _𝐺𝑖_[(] _[𝑢,𝑣]_[)] , _𝑇𝑖_ is the _𝑖_ th latent defect candidate of the test image, _𝐺𝑖_[(] _[𝑢,𝑣]_[)] is corresponding sliding window of the _𝑖_ th latent defect candidate on searched image _𝐺𝑖, 𝑢_ ∈[0 _,_ 2 _𝑑_ ] _, 𝑣_ ∈[0 _,_ 2 _𝑑_ ]. _𝑑_ is the enlarged distance of searched range. Here, _𝐺𝑖_ is cropped from _𝐺𝑀_ image based on the same location of _𝑇𝑖_ with an enlarged distance _𝑑_ . _𝑁_ is the number of Canny feature points of image _𝑇𝑖_ . _𝐺𝑥[𝐺] 𝑗[𝑖]_ and _𝐺𝑦[𝐺] 𝑗[𝑖]_ are gradient values in _𝑥_ and _𝑦_ direction of the _𝑗_ th feature point of _𝐺𝑖_ , respectively. _𝐺𝑥[𝑇] 𝑗[𝑖]_[and] _𝐺𝑦[𝑇] 𝑗[𝑖]_ are gradient values in _𝑥_ and _𝑦_ direction of the _𝑗_ th feature point of _𝑇𝑖_ , respectively. The above gradient values are all computed via the sobel operator. _𝑀𝑖_ is the _𝑖_ th latent defect candidate mask generated by Fig. 5. ‘‘&’’ represents the image bitwise AND operation. The _𝐹_ ( _𝑟𝑗 , 𝑚𝑗_ ) is a nonlinear activation function, _𝑇𝑟_ and _𝑇𝑚_ are specified thresholds. 

6 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [367 x 215] intentionally omitted <==**

**Fig. 8.** _𝑇_ 2 _𝐺_ gradient matching diagram. _𝑇𝑖_ is considered as template sub-image, _𝐺𝑖_ is considered as searched image, _𝐺𝑖_[(] _[𝑢,𝑣]_[)] is a sliding window starting from coordinate ( _𝑢, 𝑣_ ) with size ‘‘ _𝑤, ℎ_ ’’. The size of _𝐺𝑀_ , _𝐺𝑖_ and _𝑇𝑖_ is ‘‘ _𝑊, 𝐻_ ’’, ‘‘ _𝑤_ +2 _𝑑, ℎ_ +2 _𝑑_ ’’ and ‘‘ _𝑤, ℎ_ ’’, respectively. Here, _𝐺𝑖_ is cropped from _𝐺𝑀_ image based on the same location of _𝑇𝑖_ with an enlarged distance _𝑑_ . _𝑑_ is a critical parameter which is introduced to counteract the local deformation of the test image. 

**==> picture [375 x 217] intentionally omitted <==**

**Fig. 9.** _𝐺_ 2 _𝑇_ gradient matching diagram. _𝑇𝑖_[(] _[𝑢,𝑣]_[)] is a sliding window starting from coordinate ( _𝑢, 𝑣_ ) with size ‘‘ _𝑤, ℎ_ ’’. The input size of _𝐺𝑀_ , _𝐺𝑖_ and _𝑇𝑖_ is ‘‘ _𝑊, 𝐻_ ’’, ‘‘ _𝑤, ℎ_ ’’ and ‘‘ _𝑤_ + 2 _𝑑, ℎ_ + 2 _𝑑_ ’’, respectively. 

## _3.5.3. Twice gradient matching for defect detection_ 

Based on Eq. (10), the subsequent step is to perform defect detection with the proposed similarity measure. For all the latent defect candidates extracted from Section 3.3, the similarity between each subtest image and sub-GM image is required to measure. As illustrated in Fig. 8, _𝑇_ 2 _𝐺_ gradient matching represents that the _𝑇𝑖_ and the _𝐺𝑖_ are considered as a template sub-image and a searched sub-image respectively. Meanwhile, the _𝑇_ 2 _𝐺_ gradient matching is required to be performed on each sliding window ( _𝐺𝑖_[(] _[𝑢,𝑣]_[)] ). This idea is aimed at releasing the influence of local deformation. And the basis of this idea is that if the corresponding features cannot be matched in a certain neighborhood, then this region must be a defect. After the comparison of all sliding windows, a set of similarity scores is obtained, and the highest score will be considered as the final score ( _𝑆𝑖[𝑇]_[2] _[𝐺]_ ) of this _𝑖_ th latent defect candidate. Also, similar operations are applied to other latent defect candidates. 

However, _𝑇_ 2 _𝐺_ gradient matching fails to detect missing print, due to the absence of its gradient features on the test image. Correspondingly, in terms of _𝐺_ 2 _𝑇_ gradient matching, _𝐺𝑖_ and _𝑇𝑖_ are regarded as a template sub-image and a searched sub-image respectively, as presented in Fig. 9. After the comparison of all sliding windows, the highest score will be considered as the final score ( _𝑆𝑖[𝐺]_[2] _[𝑇]_ ) of the _𝑖_ th latent defect candidate. In contrast to _𝑇_ 2 _𝐺_ , _𝐺_ 2 _𝑇_ gradient matching yields to false detection on overprint whose gradient feature is also not present on the _𝐺𝑀_ image. Based on the aforementioned analysis, twice gradient matchings ( _𝑇_ 2 _𝐺_ & _𝐺_ 2 _𝑇_ ) are demanded to detect defects of missing print and overprint simultaneously. 

Furthermore, twice gradient matching is tactfully fused through similarity scores. Here, we choose the minimum score of _𝐺_ 2 _𝑇_ and _𝑇_ 2 _𝐺_ as the final similarity score of the _𝑖_ th latent defect candidate, as defined by Eq. (20). The reason is that defects tend to have lower similarity scores. Taking the missing print detection as an example, the _𝑇_ 2 _𝐺_ 

7 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**Table 1** 

Summary of training datasets of printed labels. 

|Training|dataset|Original image size|Image patch size|Number of total|Number of total defects|
|---|---|---|---|---|---|
|||(_𝑊𝑖𝑑𝑡ℎ_×_𝐻𝑒𝑖𝑔ℎ𝑡_×_𝐶ℎ𝑎𝑛𝑛𝑒𝑙𝑠_)|(_𝑊𝑖𝑑𝑡ℎ_×_𝐻𝑒𝑖𝑔ℎ𝑡_×_𝐶ℎ𝑎𝑛𝑛𝑒𝑙𝑠_)|image patches|(each patch contains a defect)|
|Alex||2768 × 1584 × 3|256 × 256 × 3|150|150|
|Com||2985 × 2385 × 3|256 × 256 × 3|200|200|
|Cons||1210 × 1396 × 3|256 × 256 × 3|200|200|
|Dev||2482 × 1457 × 3|256 × 256 × 3|200|200|
|Don||3300 × 1316 × 3|256 × 256 × 3|200|200|
|Fire||3248 × 2384 × 3|256 × 256 × 3|260|260|
|Hello||2160 × 1344 × 3|256 × 256 × 3|260|260|
|Jack||2694 × 1568 × 3|256 × 256 × 3|200|200|
|Lice||1389 × 680 × 3|256 × 256 × 3|38|38|
|Modo||1041 × 806 × 3|256 × 256 × 3|149|149|
|Mohu||689 × 703 × 3|256 × 256 × 3|38|38|
|Nom||1644 × 1414 × 3|256 × 256 × 3|200|200|
|Pow||2784 × 1520 × 3|256 × 256 × 3|290|290|
|Tvbox||1267 × 1214 × 3|256 × 256 × 3|200|200|
|Ubiq||900 × 873 × 3|256 × 256 × 3|200|200|
|War||833 × 833 × 3|256 × 256 × 3|200|200|



gradient matching gets a higher similarity score than _𝐺_ 2 _𝑇_ , and only the lower score can indicate it is a defect. 

**==> picture [252 x 11] intentionally omitted <==**

As shown in Table 8, the results of the ablation experiment prove the effectiveness of the _𝑇_ 2 _𝐺_ and _𝐺_ 2 _𝑇_ twice gradient matchings. 

Finally, for a latent defect candidate, if the final score _𝑆𝑖_ is less than a threshold _𝑇𝑠𝑐𝑜𝑟𝑒_ and the pixel area is greater than a threshold _𝑇𝑎𝑟𝑒𝑎_ , it will be judged as a defect. Otherwise, it is an artifact. 

## **Table 2** 

Summary of test datasets of printed labels. 

|Test dataset|Size|Number of total|Number of total|
|---|---|---|---|
||(_𝑊𝑖𝑑𝑡ℎ_×_𝐻𝑒𝑖𝑔ℎ𝑡_×_𝐶ℎ𝑎𝑛𝑛𝑒𝑙𝑠_)|images|defects|
|Label-1|754 × 980 × 3|1490|15,185|
|Label-2|1249 × 664 × 3|1464|14,642|
|Label-3|1092 × 714 × 3|1475|14,801|



## _4.2. Evaluation metrics_ 

## **4. Experiments** 

## _4.1. Dataset and artificial defect simulation_ 

Our experiments were conducted on 19 types of printed labels collected in a factory. 16 of them are utilized for CNN training and the other 3 are used for performance comparison. An industrial camera obtains original images with a resolution of 4088 × 3072, and these images are clipped to the size of the detected target. Then, the clipped images are aligned by feature matching as described in Section 3.2. Most of them are defect-free, and a _𝐺𝑀_ image is manually selected by human experience. Unfortunately, very few defects can be found in the real world. We randomly create artificial defects for each image to address this issue, using traditional image processing techniques. There are six types of defects, including overprint, missing print, fuzzy defect, color spot, short linear defect, and long linear defect. Since overprint and missing print are more general, the probabilities of defect types are set to [0.2, 0.2, 0.15, 0.15, 0.15, 0.15], respectively. Each defect type is randomly generated based on the above probabilities. Manual annotation is not needed since we recorded defect locations in XML format. Fig. 2 demonstrates typical examples of each type. 

In terms of the training set, Table 1 demonstrates a summary of training datasets of printed labels. To enjoy a great diversity of training samples, we utilize 16 types of printed labels for CNN training, with a total of 2985 original images. We get image patches with a size of 256 × 256 × 3 by clipping each image. And for each image patch, only one defect is randomly generated based on the above probabilities. Fig. 10 shows some representative samples of training datasets. In terms of the test set, Table 2 gives details of test datasets (Label-1, Label-2 and Label-3), which consist of 4429 images. And we randomly create ten artificial defects for each image of test datasets. The total defect numbers are 15,185, 14,642, and 14,801, respectively. The total defects include real and artificial defects. Only 285, 2, and 51 real defects exist in Label-1, Label-2, and Label-3, whose image sizes are 754 × 980 × 3, 1249 × 664 × 3 and 1092 × 714 × 3, respectively. Fig. 11 shows some representative samples of the printed label datasets. 

To quantitatively characterize the performance of the proposed method, we calculated the recall ( _𝑅_ ), precision ( _𝑃_ ), false negative rate (FNR) and _𝐹_ 1 score in object level. Recall, precision and FNR are defined as below: 

**==> picture [252 x 9] intentionally omitted <==**

**==> picture [252 x 30] intentionally omitted <==**

where true positive ( _𝑇𝑃_ ) represents real defects that are correctly predicted as defects, _𝐹𝑃_ corresponds to non-defects that are incorrectly predicted as defects, false negative ( _𝐹𝑁_ ) corresponds to real defects that are incorrectly identified as non-defects. _𝐹_ 1 score is defined as follows: 

**==> picture [252 x 9] intentionally omitted <==**

If the intersection of unit (IoU) with ground truth box is larger than 0.001, the detection is a _𝑇𝑃_ . 

## _4.3. Implementation details_ 

Our defect detection programs are conducted in C++ with OpenCV, running on a computer server with Intel(R) Xeon(R) E5-2620 CPU@2.10 GHz, Nvidia RTX2080 Ti GPU (Here, the GPU is only used for the assessment of deep learning methods), 32 GB RAM, Ubuntu 16.04 OS. The defect simulation program is conducted in Python 3.6. _𝑇𝑓𝑖𝑙𝑡𝑒𝑟_ , _𝑇𝑠𝑐𝑜𝑟𝑒_ , and _𝑇𝑎𝑟𝑒𝑎_ are set to 20, 0.75, and 5, respectively. We also use openMP (Dagum & Menon, 1998) to accelerate the proposed algorithm and set the parallel thread parameter to 12. 

For SSIM (Wang et al., 2004) and RTPDS (Shankar et al., 2009), both are implemented in C++ by OpenCV. In terms of DSIM (Vans et al., 2011), we implement it separately on R, G, B color planes in C++. The resulting error images are OR’ed together to obtain a final error map. The best matching _𝑘𝑑𝑠𝑖𝑚_ × _𝑘𝑑𝑠𝑖𝑚_ pixel neighborhood is set to 5 × 5, and a window of size _𝑊𝑑𝑠𝑖𝑚_ × _𝑊𝑑𝑠𝑖𝑚_ is also set to 5 × 5 during the 

8 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [367 x 334] intentionally omitted <==**

**Fig. 10.** Some representative samples of training datasets. 

comparison experiment. The similarity score threshold _𝑇𝑠𝑐𝑜𝑟𝑒_ is set to 0.75. For color planes, openMP is also used for accelerating. The above traditional comparison methods are performed based on ROIs extracted by LDCE instead of an entire image. 

For FCN-VGG16 (Long et al., 2015), DeepLabV3+ (Chen et al., 2018; Valente et al., 2020), we train the models with 2985 random image patches with the size 256×256×3, 80% for training, 20% for validation. The models are optimized using Adam with a mini-batch size of 16. The learning rate is set to 0.001. Please note that, the training images are in the training datasets as described in Table 1. 

## _4.4. Comparison with baselines and time complexity_ 

Table 3 illustrates several existing baselines for performance comparisons to demonstrate the effectiveness of the proposed method. The proposed method yields the highest mean _𝐹_ 1 score of 0.9702, which is a new state-of-the-art performance. Further, our method clearly outperforms these existing baselines, especially for DSIM (0.8468), FCN-VGG16 (0.7647), DeepLabV3+ (0.5558) and Valente et al. (2020) (0.5488) with improvements of 12.34%, 20.55%, 41.44% and 42.14%, respectively. In addition, our method achieves the highest scores in all performance metrics and makes comparative results, except for RTPDS achieving the best recall. However, RTPDS gets the worst mean _𝐹_ 1 score (0.3816). Note that, compared with our proposed method, the original FCN-VGG16 and DeepLabV3+ only take the test image as input, rather than an image pair (test and _𝐺𝑀_ image). That is the original design of their network input. In addition, Valente et al. (2020) takes both _𝐺𝑀_ and test image as input. However, the performance of Valente et al. (2020) is still worse than our method. 

In terms of FP and FN, Table 4 demonstrates that the proposed method has a lower misclassification rate compared to other methods, with a minimum of FP (34.33). Although RTPDS reaches the minimum FN (66.33), it has the highest FP (48,043.67), i.e., maximum false detection. In terms of the mean detection times, compared with the traditional method SSIM (1244.65 ms) and DSIM (1637.01 ms), our proposed method (263.62 ms) obviously achieves in a shorter time. Therefore, in the absence of a GPU, our method still meets the realtime requirements of the industrial. Although DeepLabV3+ gains the shortest detection time, its operation requires a GPU, which means high hardware costs. 

Table 5 illustrates the time-consuming of defect detection increases linearly with image size. We choose dataset Label-2 for the experiment since it has the largest image size. Images are resized with different scale rates. After that, we perform defect detection and record the average time-consuming. Even the image size increases to 2498 × 1328, the time-consuming is still less than 1 s. 

According to Table 3, DSIM and FCN-VGG16 are close to our method in terms of _𝐹_ 1 performance. Therefore, a comparison is conducted between them. Table 6 exhibits the misclassification of three methods for detecting various types of defects. The performance of DSIM is the worst compared to the other two methods. Especially, it is almost impossible for DSIM to detect fuzzy print defects. And its average FNR of all defect classes reaches 0.2347, i.e., more than one-fifth of defects are detected incorrectly. Therefore, DSIM cannot be directly applied to printed label defect detection. Our method has the best performance in detecting four classes of defects, whereas FCN-VGG16 has the best performance in the remaining two classes. Therefore, our method is capable of more detection scenarios. And the average FNR of FCN-VGG16 for all classes is 0.0328 higher than that of our method. Therefore, our method is better than FCN-VGG16. 

9 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [441 x 307] intentionally omitted <==**

**Fig. 11.** Some representative samples of test datasets. 

**Table 3** 

Comparison with existing baselines on datasets (Label-1, Label-2 and Label-3) in terms of recall, precision and _𝐹_ 1 scores. For each column, the best result is highlighted in bold. 

|Comparison with existing baselines on d|atasets (Label-1, Label-2 and Label-3) in te|rms of recall, precision and _𝐹_1 scores. For|each column, the best result is highlighted in bold.|
|---|---|---|---|
|Method|Label-1<br>Recall<br>Precision<br>_𝐹_1|Label-2<br>Recall<br>Precision<br>_𝐹_1|Label-3<br>Mean<br>Recall<br>Precision<br>_𝐹_1<br>_𝐹_1|
|SSIM (Wang et al., 2004)<br>RTPDS (Shankar et al., 2009)<br>DSIM (Vans et al., 2011)<br>FCN-VGG16 (Long et al., 2015)<br>DeepLabV3+ (Chen et al., 2018)<br>Valente et al. (2020)<br>Ours|0.9273<br>0.2687<br>0.4167<br>**0.9953**<br>0.2552<br>0.4062<br>0.7805<br>0.9959<br>0.8751<br>0.9111<br>0.6246<br>0.7411<br>0.8242<br>0.3356<br>0.4770<br>0.5445<br>0.7688<br>0.6375<br>0.9397<br>**0.9998**<br>**0.9688**|0.9855<br>0.2291<br>0.3718<br>**0.9952**<br>0.2213<br>0.3621<br>0.7541<br>0.9990<br>0.8594<br>0.9178<br>0.9441<br>0.9308<br>0.7181<br>0.8007<br>0.7571<br>0.2746<br>0.9968<br>0.4305<br>0.9459<br>**0.9999**<br>**0.9721**|0.9072<br>0.2443<br>0.3849<br>0.3911<br>**0.9962**<br>0.2322<br>0.3766<br>0.3816<br>0.7607<br>0.8569<br>0.8059<br>0.8468<br>0.9058<br>0.4740<br>0.6223<br>0.7647<br>0.7808<br>0.2997<br>0.4332<br>0.5558<br>0.4237<br>0.9116<br>0.5785<br>0.5488<br>0.9475<br>**0.9931**<br>**0.9697**<br>**0.9702**|



## **Table 4** 

Comparison with existing baselines on datasets (Label-1, Label-2 and Label-3) in terms of the FP, FN, and detection time. For each column, the best result is highlighted in bold. 

|bold.|||||
|---|---|---|---|---|
|Method|Label-1<br>FP<br>FN<br>Time<br>(ms)|Label-2<br>FP<br>FN<br>Time<br>(ms)|Label-3<br>FP<br>FN<br>Time<br>(ms)|Mean|
|||||FP<br>FN<br>Time<br>(ms)|
|SSIM (Wang et al., 2004)<br>RTPDS (Shankar et al., 2009)<br>DSIM (Vans et al., 2011)<br>FCN-VGG16 (Long et al., 2015)<br>DeepLabV3+ (Chen et al., 2018)<br>Valente et al. (2020)<br>Ours|38,316<br>1104<br>1159.06<br>44,118<br>**72**<br>254.63<br>49<br>3333<br>1489.26<br>8314<br>1350<br>96.24<br>24,778<br>2670<br>**81.30**<br>2486<br>6917<br>103.77<br>**3**<br>916<br>248.32|48,548<br>212<br>1088.79<br>51,257<br>**71**<br>309.43<br>11<br>3601<br>1284.83<br>795<br>1204<br>107.37<br>2617<br>4128<br>**85.06**<br>13<br>10,622<br>114.25<br>**2**<br>792<br>298.49|41,544<br>1374<br>1486.10<br>48,756<br>**56**<br>307.11<br>1880<br>3542<br>2136.94<br>14,880<br>1394<br>98.79<br>27,000<br>3245<br>**84.02**<br>608<br>8530<br>106.91<br>**98**<br>777<br>244.06|42,802.67<br>896.67<br>1244.65<br>48,043.67<br>**66.33**<br>290.39<br>646.67<br>3492.00<br>1637.01<br>7996.33<br>1316.00<br>100.80<br>18,131.67<br>3347.67<br>**83.46**<br>1035.67<br>8689.67<br>108.31<br>**34.33**<br>828.33<br>263.62|



## **Table 5** 

Time-consuming for different image sizes on dataset Label-2. Images from dataset Label-2 are resized with different scale rate, and average detection times are measured respectively. It indicates that the detection time increases linearly with the image size. 

|Scale rate|0.2|0.4|0.6|0.8|1.0|1.2|1.4|1.6|1.8|2.0|
|---|---|---|---|---|---|---|---|---|---|---|
|Size|249 × 132|499 × 265|749 × 398|999 × 531|1249 × 664|1498 × 796|1748 × 929|1998 × 1062|2248 × 1195|2498 × 1328|
|Detection time (ms)|35.52|67.6|125.86|177.03|298.49|328.64|531.32|662.80|771.85|981.25|



10 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

## **Table 6** 

Misclassifications of various defects on test datasets (Label-1, Label-2 and Label-3). For the mean FNR, the best results are highlighted in bold. 

|Defect class<br>Method|Label-1|Label-2|Label-3<br><br>Defects number FN<br>FNR<br>|Mean FNR|
|---|---|---|---|---|
||Defects number FN<br>FNR|Defects number FN<br>FNR||Each class All classes|
|Overprint defects<br>DSIM (Vans et al., 2011)<br>Missing print defects<br>Fuzzy print defects<br>Color spot print defects<br>Short linear print defects<br>Long linear print defects|2882<br>608<br>0.2110 <br>2997<br>29<br>0.0097 <br>2205<br>2146 0.9732 <br>2618<br>234<br>0.0894 <br>2993<br>297<br>0.0992 <br>1490<br>19<br>0.0128|2931<br>572<br>0.1952 <br> 2931<br>9<br>0.0031 <br> 2246<br>2185 0.9728 <br> 2262<br>390<br>0.1724 <br> 2702<br>422<br>0.1562 <br> 1570<br>23<br>0.0146|2128<br>350<br>0.1645 <br> 3591<br>156<br>0.0434 <br> 2267<br>2126 0.9378 <br> 2366<br>491<br>0.2075 <br> 3033<br>402<br>0.1325 <br> 1416<br>17<br>0.0120|0.1902<br>0.2347<br>0.0187<br>0.9613<br>0.1564<br>0.1293<br>0.0131|
|Overprint defects<br>FCN-VGG16 (Long et al., 2015)<br>Missing print defects<br>Fuzzy print defects<br>Color spot print defects<br>Short linear print defects<br>Long linear print defects|2882<br>484<br>0.1679 <br>2997<br>134<br>0.0447 <br>2205<br>15<br>0.0068 <br>2618<br>317<br>0.1211 <br>2993<br>339<br>0.1133 <br>1490<br>61<br>0.0409|2931<br>255<br>0.0870 <br> 2931<br>95<br>0.0324 <br> 2246<br>10<br>0.0045 <br> 2262<br>348<br>0.1538 <br> 2702<br>423<br>0.1566 <br> 1570<br>73<br>0.0465|2128<br>190<br>0.0893 <br> 3591<br>343<br>0.0955 <br> 2267<br>22<br>0.0097 <br> 2366<br>319<br>0.1348 <br> 3033<br>410<br>0.1352 <br> 1416<br>110<br>0.0777|0.1147<br>0.0885<br>0.0575<br>**0.0070**<br>**0.1366**<br>0.1350<br>0.0550|
|Overprint defects<br>Ours<br>Missing print defects<br>Fuzzy print defects<br>Color spot print defects<br>Short linear print defects<br>Long linear print defects|2882<br>278<br>0.0965 <br>2997<br>43<br>0.0143 <br>2205<br>42<br>0.0190 <br>2618<br>413<br>0.1578 <br>2993<br>130<br>0.0434 <br>1490<br>10<br>0.0067|2931<br>117<br>0.0399 <br> 2931<br>3<br>0.0010 <br> 2246<br>12<br>0.0053 <br> 2262<br>519<br>0.2294 <br> 2702<br>139<br>0.0514 <br> 1570<br>2<br>0.0013|2128<br>95<br>0.0446 <br> 3591<br>18<br>0.0050 <br> 2267<br>21<br>0.0093 <br> 2366<br>496<br>0.2096 <br> 3033<br>138<br>0.0455 <br> 1416<br>9<br>0.0064|**0.0603**<br>**0.0557**<br>**0.0068**<br>0.0112<br>0.1989<br>**0.0468**<br>**0.0048**|



## **Table 7** 

The performance of PLDD on datasets Label-1 and Label-2 under various _𝑛_ . For each column of the mean result, the best result is highlighted in bold. 

|_𝑛_|Label-1<br>Recall<br>Precision<br>_𝐹_1<br>Total time<br>(s)<br>FP<br>FN|Label-2<br>Recall<br>Precision<br>_𝐹_1<br>Total time<br>(s)<br>FP<br>FN|Mean|
|---|---|---|---|
||||_𝐹_1<br>Total time<br>(s)<br>FP<br>FN|
|1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9|0.9155<br>0.9997<br>0.9558<br>2286.34<br>4<br>1283<br>0.9316<br>0.9996<br>0.9644<br>661.30<br>6<br>1039<br>0.9363<br>0.9996<br>0.9669<br>404.81<br>5<br>967<br>0.9397<br>0.9998<br>0.9688<br>369.99<br>3<br>916<br>0.9403<br>0.9998<br>0.9691<br>377.65<br>3<br>907<br>0.9370<br>0.9998<br>0.9671<br>359.62<br>3<br>956<br>0.9419<br>0.9998<br>0.9700<br>342.78<br>3<br>883<br>0.9353<br>0.9996<br>0.9664<br>353.11<br>5<br>983<br>0.8938<br>0.9997<br>0.9438<br>370.66<br>4<br>1613|0.9145<br>0.9870<br>0.9520<br>2352.27<br>178<br>1179<br>0.9418<br>0.9963<br>0.9683<br>714.59<br>51<br>852<br>0.9438<br>0.9987<br>0.9705<br>447.00<br>18<br>823<br>0.9459<br>0.9999<br>0.9721<br>436.99<br>2<br>792<br>0.9310<br>0.9982<br>0.9635<br>392.84<br>24<br>1010<br>0.9370<br>0.9999<br>0.9675<br>398.51<br>1<br>922<br>0.9237<br>0.9999<br>0.9603<br>381.77<br>2<br>1117<br>0.9475<br>0.9999<br>0.9730<br>402.53<br>2<br>769<br>0.9071<br>0.9990<br>0.9509<br>379.92<br>13<br>1360|0.9539<br>2319.31<br>91.00<br>1231.00<br>0.9664<br>687.95<br>28.50<br>945.50<br>0.9687<br>425.91<br>11.50<br>895.00<br>**0.9705**<br>403.49<br>2.50<br>**854.00**<br>0.9663<br>385.25<br>13.50<br>958.50<br>0.9673<br>379.07<br>**2.00**<br>939.00<br>0.9652<br>**362.28**<br>2.50<br>1000.00<br>0.9697<br>377.82<br>3.50<br>876.00<br>0.9474<br>375.29<br>8.50<br>1486.50|



## _4.5. Analysis of adjustment parameter 𝑛 in LDCE algorithm_ 

As mentioned in LDCE, test images are divided into _𝑛_ × _𝑛_ subimages. To verify how this value of _𝑛_ affects performance, we conducted the experiment by applying different _𝑛_ , _𝑛_ ∈{1 _,_ 2 _,_ 3 _,_ … _,_ 9}. Table 7 illustrates test results which are based on datasets Label-1 and Label2. Without the loss of generalization, we only verified test results on Label-1 and Label-2. Based on the results of Table 7, our findings can be summarized as follows: 

- (1) As the value of _𝑛_ reduces, the total test time becomes larger and larger. Especially, the mean total time reaches 2319.31 s when _𝑛_ = 1. The reason is that there is no artifact elimination under this condition, and amounts of artifacts increase the detection time significantly. The number of _𝐹𝑁_ and _𝐹𝑃_ gradually increases, and the score of _𝐹_ 1 gradually decreases. 

- (2) As the value of _𝑛_ increases, the number of _𝐹𝑁_ gradually increases, and the score of _𝐹_ 1 decreases gradually. _𝑛_ = 9 has the highest _𝐹𝑁_ (1486.50) and lowest _𝐹_ 1 (0.9474). _𝑛_ = 4 has the highest _𝐹_ 1 (0.9705) and lowest _𝐹𝑁_ (854.00). Here, we give an analysis for this. As n gets larger and larger, an image is divided into smaller sub-images. As a result, some defects are cut into small pieces. After LDCE, it is difficult to maintain the integrity of original defects, which will increase the number of _𝐹𝑁_ . 

- (3) In summary, to balance _𝐹_ 1, total time, _𝐹𝑃_ and _𝐹𝑁_ , the best performance is achieved when _𝑛_ = 4. The reason is that _𝑛_ = 4 has the highest _𝐹_ 1 (0.9705), the lowest _𝐹𝑁_ (854.00), and _𝐹𝑃_ (2.50). The _𝐹𝑃_ (2.50) is very close to the lowest _𝐹𝑃_ (2.00). Also, the total time (403.49 s) is acceptable because it still meets the requirement of real-time. 

**==> picture [154 x 151] intentionally omitted <==**

**Fig. 12.** Some examples of SSIM vs. ICSM similarity measure. (a) and (c) are completely different, but their SSIM similarity scores (0.83) are exactly the same, as well as (b) and _𝐺𝑀_ . Further, (d) and _𝐺𝑀_ obviously are different, but their SSIM score is as high as 0.90. In terms of ICSM, all of theirs scores are calculated as 0, which is consistent with human vision. 

## _4.6. Ablation studies and quantitative analysis_ 

In defect detection, the image which is similar to _𝐺𝑀_ image should have a high similarity score. In contrast, the image which is different from _𝐺𝑀_ image should have a low similarity score. Only in this way can defects and artifacts be easily distinguished. However, Fig. 12 demonstrates that the SSIM-based similarity measure cannot satisfy defect detection in certain circumstances, and may result in amounts 

11 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

**==> picture [220 x 142] intentionally omitted <==**

**Fig. 13.** Comparison between original cosine similarity and ICSM. 83 defective samples are presented. 

of false detection in practice. By comparison, our ICSM method provides discriminative scores which are consistent with human visual characteristics. 

In addition, as shown in Fig. 13, a comparison between original cosine similarity measure and ICSM is performed based on random 83 defective samples. Obviously, the ICSM is relatively more discriminative than the original one since the overall scores are decreased. For defective samples, it is better to obtain lower similarity scores. 

Furthermore, we conducted additional ablation experiments on the three datasets to evaluate the effectiveness of different improved components. There are four improved components: mask, ICSM, _𝑇_ 2 _𝐺_ , and _𝐺_ 2 _𝑇_ . In this paper, we remove an improved component each time to demonstrate its effectiveness. In Table 8, the method without mask, without ICSM, without _𝐺_ 2 _𝑇_ , and without _𝑇_ 2 _𝐺_ are applied for performance comparisons, and their corresponding _𝐹_ 1 scores are 0.9500, 0.9093, 0.9474 and 0.7649. By contrast, the _𝐹_ 1 score (0.9702) computed by the proposed method benefits from the integration of the four components, and it has an improvement of 2.02%, 6.09%, 2.28%, and 20.53%, respectively. The most noticeable improvement is the _𝑇_ 2 _𝐺_ component, and the second one is the ICSM component. After removing the ICSM component, the _𝐹_ 1 score drops significantly from 0.9702 to 0.9093. The proposed method also got the minimum mean FN (828) compared with any other combinations. Unfortunately, the FP (34) of the proposed method is worse than that of the method without the ICSM component. 

**Table 8** 

Comparison of ablation study with four improved components for the proposed method. The best result is highlighted in bold. 

|Dataset|Mask<br>ICSM<br>_𝐺_2_𝑇_<br>_𝑇_2_𝐺_<br>Recall<br>Precision<br>_𝐹_1<br>FP<br>FN|
|---|---|
|Label-1<br>Label-2<br>Label-3<br>Mean|�<br>�<br>�<br>�<br>0.9397<br>0.9998<br>**0.9688**<br>3<br>**916**<br>�<br>�<br>�<br>0.9104<br>0.9999<br>0.953<br>2<br>1361<br>�<br>�<br>�<br>0.8169<br>0.9999<br>0.8992<br>**1**<br>2781<br>�<br>�<br>�<br>0.8853<br>0.9998<br>0.9391<br>3<br>1741<br>�<br>�<br>�<br>0.5768<br>0.9998<br>0.7316<br>2<br>6426|
||�<br>�<br>�<br>�<br>0.9459<br>0.9999<br>**0.9721**<br>2<br>**792**<br>�<br>�<br>�<br>0.8985<br>0.9998<br>0.9465<br>2<br>1486<br>�<br>�<br>�<br>0.8563<br>1<br>0.9226<br>**0**<br>2104<br>�<br>�<br>�<br>0.9136<br>0.9999<br>0.9548<br>1<br>1265<br>�<br>�<br>�<br>0.6987<br>0.9999<br>0.8226<br>1<br>4412|
||�<br>�<br>�<br>�<br>0.9475<br>0.9931<br>**0.9697**<br>98<br>**777**<br>�<br>�<br>�<br>0.9122<br>0.9919<br>0.9504<br>110<br>1300<br>�<br>�<br>�<br>0.8287<br>0.9993<br>0.9061<br>**8**<br>2535<br>�<br>�<br>�<br>0.9064<br>0.9945<br>0.9484<br>74<br>1385<br>�<br>�<br>�<br>0.5894<br>0.9955<br>0.7405<br>39<br>6077|
||�<br>�<br>�<br>�<br>0.9444<br>0.9976<br>**0.9702**<br>34<br>**828**<br>�<br>�<br>�<br>0.907<br>0.9972<br>0.9500<br>38<br>1382<br>�<br>�<br>�<br>0.834<br>0.9997<br>0.9093<br>**3**<br>2473<br>�<br>�<br>�<br>0.9018<br>0.9981<br>0.9474<br>26<br>1464<br>�<br>�<br>�<br>0.6216<br>0.9984<br>0.7649<br>14<br>5638|



**==> picture [150 x 143] intentionally omitted <==**

**Fig. 14.** Qualitative printed label defect detection results of the proposed framework. For each defective ROI, the number before the comma indicates the similarity score, and the number after the comma denotes the area of defective pixels. 

## _4.7. Qualitative results_ 

Table 9 visualizes a comparison result of artifact elimination among RGB absolute difference and LDCE . We observe that amounts of artifacts do exist after RGB absolute difference. However, these artifacts are significantly eliminated after LDCE. Fig. 14 further demonstrates some detection results of different defects types, including overprint, missing print, fuzzy defect, color spot, short linear defect, and long linear defect. Furthermore, Fig. 15 visualizes comparison among compared methods and PLDD (Label-1). Compared methods do exist some FP or FN results to a certain extent. 

## **5. Conclusions and future work** 

Few of existing printed label defect detection approaches pay attention to artifact elimination and the better generalization for unseen defects of the printed label. In this paper, to solve these problems, we propose a novel printed label defect detection (PLDD) framework. Firstly, artifact elimination and latent defect candidates extraction are performed via the LDCE algorithm in PLDD, which removes artifacts notably while preserving the defects. Secondly, twice gradient 

matchings ( _𝑇_ 2 _𝐺_ & _𝐺_ 2 _𝑇_ ) based on improved cosine similarity measures are executed on defect candidates only. The mask mechanism is also introduced to eliminate the influence of background gradient features around the latent defect candidates. Meanwhile, three datasets are applied to validate the generalizability of the proposed framework. Finally, comparison experiments and ablation studies are conducted, and the results exhibit that the proposed method achieves state-of-the-art performance. 

In PLDD, image registration is the first step of our approach and is also the key point in subsequent steps. However, there do still exist some artifacts after LDCE, especially in the case of large non-rigid deformation. Therefore, how to improve image registration performance for large deformation is the main direction of our future work. We observe that some unsupervised registration methods based on deep learning have achieved remarkable results in medical images. However, few of them pay attention to the registration of industrial images. In addition, some low-contrast defects are still not easily detected, and this will be improved in future work. 

12 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

## **Table 9** 

Comparison of artifact elimination between RGB absdiff and LDCE difference. The columns of ‘‘RGB absdiff‘‘ and ‘‘LDCE difference’’ are the enhanced visualization by applying a hot colormap. 

**==> picture [346 x 222] intentionally omitted <==**

**==> picture [346 x 237] intentionally omitted <==**

**Fig. 15.** Visualization comparison among SSIM, RTPDS, DSIM, FCN-VGG16, DeepLabV3+, Valente et al. (2020) and PLDD (Label-1). The results of _𝑇𝑃_ , _𝐹𝑃_ , and _𝐹𝑁_ are annotated with red, green, and yellow bounding boxes, respectively. (a) is the ground truth image whose defects are annotated by LabelImg tool (Tzutalin, 2015). 

## **CRediT authorship contribution statement** 

## **Declaration of competing interest** 

**Dongming Li:** Conceptualization, Methodology, Software, Writing – original draft, Writing – review & editing, Data curation. **Jinxing Li:** Writing – review & editing, Investigation. **Yuanyi Fan:** Software, Writing – review & editing. **Guangming Lu:** Supervision, Project administration, Funding acquisition. **Jie Ge:** Investigation, Visualization. **Xiaoyang Liu:** Validation, Resources. 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## **Acknowledgments** 

This work was supported in part by the NSFC, China fund (62176077, 61906162), in part by the Guangdong Basic and Applied Basic Research 

13 

_D. Li et al._ 

_Expert Systems With Applications 204 (2022) 117372_ 

Foundation under Grant 2019Bl515120055, in part by the Shenzhen Luan, C., Jing, Z., & Zuo, J. (2021). A defect-sensitive loss function based on siamese Key Technical Project, China under Grant 2020N046, in part by the network to defect detection with imbalanced samples. In _Journal of physics:_ Shenzhen Fundamental Research Fund under Grant JCYJ20210324132210025, _Conference series, Vol. 1802_ . IOP Publishing, Article 042085. Ma, B., Zhu, W., Wang, Y., Wu, H., Yang, Y., Fan, H., & Xu, H. (2017). The in part by the Medical Biometrics Perception and Analysis Engineerdefect detection of personalized print based on template matching. In _2017 IEEE_ ing Laboratory, Shenzhen, China, in part by Shenzhen Science and _international conference on unmanned systems (ICUS)_ (pp. 266–271). Technology Program (RCBS20200714114910193), and in part by EdNguyen, N. H. T., Perry, S., Bone, D., Le, H. T., & Nguyen, T. T. (2021). Two-stage ucation Center of Experiments and Innovations at Harbin Institute of convolutional neural network for road crack detection and segmentation. _Expert Systems with Applications_ , Article 115718. Technology, Shenzhen, China. 

- Ma, B., Zhu, W., Wang, Y., Wu, H., Yang, Y., Fan, H., & Xu, H. (2017). The defect detection of personalized print based on template matching. In _2017 IEEE international conference on unmanned systems (ICUS)_ (pp. 266–271). 

- Nguyen, N. H. T., Perry, S., Bone, D., Le, H. T., & Nguyen, T. T. (2021). Two-stage convolutional neural network for road crack detection and segmentation. _Expert Systems with Applications_ , Article 115718. 

Peng, X., Chen, Y., Xie, J., Liu, H., & Gu, C. (2010). An intelligent online presswork defect detection method and system. In _2010 second international conference on information technology and computer science_ (pp. 158–161). 

## **References** 

   - Riemersma, T. (2012). Colour metric. Retrieved from www.compuphase.com/cmetric. htm (Accessed July 25, 2021). 

- Asha, V., Bhajantri, N. U., & Nagabhushan, P. (2012). Similarity measures for automatic defect detection on patterned textures. _International Journal of Information and Communication Technology_ , _4_ (2–4), 118–131. 

   - Shankar, N., Ravi, N., & Zhong, Z. (2009). A real-time print-defect detection system for web offset printing. _Measurement_ , _42_ (5), 645–652. 

   - Tabernik, D., Šela, S., Skvarč, J., & Skočaj, D. (2020). Segmentation-based deep-learning approach for surface-defect detection. _Journal of Intelligent Manufacturing_ , _31_ (3), 759–776. 

- Bergmann, P., Löwe, S., Fauser, M., Sattlegger, D., & Steger, C. (2018). Improving unsupervised defect segmentation by applying structural similarity to autoencoders. arXiv preprint arXiv:1807.02011. 

   - Tsai, D.-M., Lin, C.-T., & Chen, J.-F. (2003). The evaluation of normalized cross correlations for defect detection. _Pattern Recognition Letters_ , _24_ (15), 2525–2535. 

- Bouchot, J.-L., Stübl, G., & Moser, B. (2011). A template matching approach based on the discrepancy norm for defect detection on regularly textured surfaces. In _Tenth international conference on quality control by artificial vision, Vol. 8000_ (p. 80000K). International Society for Optics and Photonics. 

   - Tzutalin, D. (2015). LabelImg (2015). Retrieved from GitHub repository https://github. com/tzutalin/labelImg (Accessed July 25, 2021). 

   - Valente, A., Wada, C., Neves, D., Neves, D., Perez, F., Megeto, G., Cascone, M., Gomes, O., & Lin, Q. (2020). Print defect mapping with semantic segmentation. In _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ (pp. 3551–3559). 

- Chen, Q., Jessome, R., Maggard, E., & Allebach, J. P. (2019). Segmentation-based detection of local defects on printed pages. _Electronic Imaging_ , _2019_ (10), 301. 

- Chen, L.-C., Zhu, Y., Papandreou, G., Schroff, F., & Adam, H. (2018). Encoder-decoder with atrous separable convolution for semantic image segmentation. In _Proceedings of the European conference on computer vision (ECCV)_ (pp. 801–818). 

   - Vans, M., Schein, S., Staelin, C., Kisilev, P., Simske, S. J., Dagan, R., & Harush, S. (2011). Automatic visual inspection and defect detection on variable data prints. _Journal of Electronic Imaging_ , _20_ (1), Article 013010. 

- Dagum, L., & Menon, R. (1998). OpenMP: an industry standard API for shared-memory programming. _IEEE Computational Science and Engineering_ , _5_ (1), 46–55. 

   - Verikas, A., Lundström, J., Bacauskiene, M., & Gelzinis, A. (2011). Advances in computational intelligence-based print quality assessment and control in offset colour printing. _Expert Systems with Applications_ , _38_ (10), 13441–13447. 

- Dailin, Z., Wenguang, C., & Jing, M. (2013). Detection of printed material defects based on shape template matching. _Mechanical and Electronic_ , (12), 40–44. 

- Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., & Fei-Fei, L. (2009). Imagenet: A largescale hierarchical image database. In _2009 IEEE conference on computer vision and pattern recognition_ (pp. 248–255). 

   - Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P. (2004). Image quality assessment: from error visibility to structural similarity. _IEEE Transactions on Image Processing_ , _13_ (4), 600–612. 

- Deng, Z., Yan, X., Zhang, S., & Bailey, C. P. (2020). Extremal region analysis based deep learning framework for detecting defects. arXiv preprint arXiv:2003.08525. 

   - Wu, X., Cao, K., & Gu, X. (2017). A surface defect detection based on convolutional neural network. In _International conference on computer vision systems_ (pp. 185–194). Springer. 

- Di, H., Ke, X., Peng, Z., & Dongdong, Z. (2019). Surface defect classification of steels with a new semi-supervised learning method. _Optics and Lasers in Engineering_ , _117_ , 40–48. 

   - Wu, S., Wu, Y., Cao, D., & Zheng, C. (2019). A fast button surface defect detection method based on siamese network with imbalanced samples. _Multimedia Tools and Applications_ , _78_ (24), 34627–34648. 

- Ferguson, M. K., Ronay, A., Lee, Y.-T. T., & Law, K. H. (2018). Detection and segmentation of manufacturing defects with convolutional neural networks and transfer learning. _Smart and Sustainable Manufacturing Systems_ , _2_ . 

   - Wu, J., Ye, Y., Chen, Y., & Weng, Z. (2018). Spot the difference by object detection. arXiv preprint arXiv:1801.01051. 

- Gong, W., Zhang, K., Yang, C., Yi, M., & Wu, J. (2020). Adaptive visual inspection method for transparent label defect detection of curved glass bottle. In _2020 international conference on computer vision, image and deep learning (CVIDL)_ (pp. 90–95). 

   - Yangping, W., Shaowei, X., Zhengping, Z., Yue, S., & Zhenghai, Z. (2018). Realtime defect detection method for printed images based on grayscale and gradient differences. _Journal of Engineering Science & Technology Review_ , _11_ (1). 

   - Yu, Z., Wu, X., & Gu, X. (2017). Fully convolutional networks for surface defect inspection in industrial environment. In _International conference on computer vision systems_ (pp. 417–426). Springer. 

- Haik, O., Perry, O., Chen, E., & Klammer, P. (2020). A novel inspection system for variable data printing using deep learning. In _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ (pp. 3541–3550). 

   - Zhang, E., Chen, Y., Gao, M., Duan, J., & Jing, C. (2019). Automatic defect detection for web offset printing based on machine vision. _Applied Sciences_ , _9_ (17), 3598. 

- Ilg, E., Mayer, N., Saikia, T., Keuper, M., Dosovitskiy, A., & Brox, T. (2017). Flownet 2.0: Evolution of optical flow estimation with deep networks. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ (pp. 2462–2470). 

   - Zhang, H., Jiang, L., & Li, C. (2021). CS-ResNet: Cost-sensitive residual convolutional neural network for PCB cosmetic defect detection. _Expert Systems with Applications_ , Article 115673. 

- Johnson, G. M., Song, X., Montag, E. D., & Fairchild, M. D. (2010). Derivation of a color space for image color difference measurement. _Color Research & Application_ , _35_ (6), 387–400. 

   - Zhang, K., Yan, Y., Li, P., Jing, J., Wang, Z., & Xiong, Z. (2020). Fabric defect detection using saliency of multi-scale local steering kernel. _IET Image Processing_ , _14_ (7), 1265–1272. 

- Long, J., Shelhamer, E., & Darrell, T. (2015). Fully convolutional networks for semantic segmentation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ (pp. 3431–3440). 

- Zhao, Z., Li, B., Dong, R., & Zhao, P. (2018). A surface defect detection method based on positive samples. In _Pacific rim international conference on artificial intelligence_ (pp. 473–481). Springer. 

14 

