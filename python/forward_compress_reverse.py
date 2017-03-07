from numpy import *
from sound import *
from images import *
from fft import *
from dwt import *

def forw_comp_rev_DFT(L=0, lower=-1, threshold=0, n=0, N=0):
    x, fs = audioread('sounds/castanets.wav')
    x = x.astype(complex)
    if N == 0:
        N = len(x)
    sz = len(x)
    numzeroed = 0
    for ind in range(0, sz, N):
        y = fft.fft(x[ind:(ind + N)], axis=0)
        if lower == 1:
            y[(L+1):(N-L)] = 0
        elif lower == 0:
            y[0:(N/2 - L)] = 0
            y[(N/2 + L):] = 0
        if threshold != 0:
            numzeroed += sum((abs(y) < threshold))
            y *= (abs(y) >= threshold)
        if n != 0:
            y /= 2**n
            y = around(y)
            y *= 2**n
        x[ind:(ind + N)] = fft.ifft(y, axis=0)
    x = real(x)
    x /= abs(x).max()
    if threshold != 0:
        print 100*numzeroed/float(prod(shape(x)))
    return x, fs
    
def forw_comp_rev_DFT2(f, invf, threshold):
    # TODO: f, invf
    X = CreateExcerpt()
    X = X.astype(complex)
    M, N = shape(X)[0:2]
    
    tensor_impl(X, f, f)
    tot = prod(shape(X))

    thresholdmatr = (abs(X[:,:,:]) >= threshold)
    zeroedout = tot - sum(thresholdmatr)
    X[:,:,:] *= thresholdmatr
    tensor_impl(X[:,:,:], invf, invf);
    X[:,:,:] = abs(X[:,:,:])
    mapto01(X[:,:,:])
    X[:,:,:] *= 255
    print '%f percent of samples zeroed out' % (100*zeroedout/float(tot))
    return X
    
def forw_comp_rev_DCT2(f, invf, threshold):
    X = CreateExcerpt()
    tensor_impl(X, f, f)
    tot = prod(shape(X))
  
    thresholdmatr = (abs(X[:,:,:]) >= threshold)
    zeroedout = tot - sum(thresholdmatr)
    X[:,:,:] *= thresholdmatr
    tensor_impl(X[:,:,:], invf, invf);
    mapto01(X[:,:,:])
    X[:,:,:] *= 255
    print '%f percent of samples zeroed out' % (100*zeroedout/float(tot))
    return X    
    
def forw_comp_rev_DWT(m, wave_name, lowres = 1):
    """
    Play a sound after removing either the detail or the lowres part.
    
    m: The number of resolutions
    f: The DWT kernel
    invf: The IDWT kernel
    lowres: If true, set the detail to 0 and play the lowres part. 
            If false, set the lowres part to 0 and play the detail.  
    """
    x, fs = audioread('sounds/castanets.wav')
    N = 2**17
    x = x[0:N]
    DWTImpl(x, m, wave_name)
    if lowres==1:
        x[(N/2**m):N] = 0
    else:
        x[0:(N/2**m)] = 0
    IDWTImpl(x, m, wave_name)
    x /= abs(x).max()
    return x, fs
    
def forw_comp_rev_DWT2(m, wave_name, lowres = 1):
    """
    Show an image after removing either the detail or the lowres part
    
    m: The number of resolutions
    f: The DWT kernel
    invf: The IDWT kernel
    lowres: If true, set the detail to 0 and show the lowres part. 
            If false, set the lowres part to 0 and show the detail.  
    """
    img = CreateExcerpt()
    M, N = shape(img)[0:2]
    DWT2Impl(img, m, wave_name)
    if lowres==1:
        tokeep = img[0:(M/(2**m)), 0:(N/(2**m))]
        img=zeros_like(img)
        img[0:(M/(2**m)),0:(N/(2**m))] = tokeep
    else:
        img[0:(M/2**m), 0:(N/2**m)] = 0
    IDWT2Impl(img, m, wave_name) 
    mapto01(img)
    img *= 255
    return img