
/*
================
MOBILE NAV LINKS
================
*/ 
const mobileNavs = [...document.querySelectorAll('.mobile-nav')]
const mobileNavLinks = document.querySelector('.mobile-nav-links')
const mobileNavCloseBtn = document.querySelector('.mobile-nav-close-btn')
const mobileToggleNavBtn = document.querySelector('.mobile-toggle-nav-btn')
const mobileNavBackgroundLayout = document.querySelector('.mobile-nav-background-layout')
const body = document.querySelector('body')



mobileToggleNavBtn.addEventListener('click', (e) => {
    mobileNavLinks.classList.add('show-mobile-nav-bar')
    mobileNavBackgroundLayout.style.display = 'block'
    body.style.overflow = 'hidden'

})

mobileNavCloseBtn.addEventListener('click', () => {
    mobileNavLinks.classList.remove('show-mobile-nav-bar')
    mobileNavBackgroundLayout.style.display = 'none'
    body.style.overflow = 'auto'
})

mobileNavs.forEach((nav) => {
    nav.addEventListener('click', (e) => {
        body.style.overflow = 'auto'
    })
})


/*
=============
BANNER IMAGES
=============
*/
const bannerImgContainers = [...document.querySelectorAll('.banner-img-container')]
const bannerArrowLeft = document.querySelector('.banner-arrow-left')
const bannerArrowRight = document.querySelector('.banner-arrow-right')
const TranslateBtns = [...document.querySelectorAll('.translate-btn')]
const circles = [...document.querySelectorAll('.circle')]

let index = 0

circles[0].style.background = 'white'

TranslateBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const targetElement = e.currentTarget === bannerArrowLeft ? bannerArrowLeft : bannerArrowRight
        if(targetElement === bannerArrowLeft){
            index --
        }else if(targetElement === bannerArrowRight) {
            index ++
        }
        if(index < 0){
            index = bannerImgContainers.length - 1
        }else if(index > bannerImgContainers.length - 1){
            index = 0
        }
        bannerImgContainers.forEach((img) => {
            img.style.transform = `translate(-${index * 100}%)`
        })
        circles.forEach((circle) => {
            if(circles.indexOf(circle) === index) {
                circle.style.background = 'white'
            }else {
                circle.style.background = 'rgb(90, 90, 90)'
            }
        })
    })
})


/*
===================
PRODUCT DETAIL PAGE
===================
*/ 
const productDetailToggleBtns = [...document.querySelectorAll('.product-detail-toggle-btn')]
const productDescription = document.querySelector('.product-description')
const productDetail = document.querySelector('.product-detail')
const productDescriptionArrowUp = document.querySelector('.product-description-arrow-up')
const productDescriptionArrowDown = document.querySelector('.product-description-arrow-down')
const productDetailArrowUp = document.querySelector('.product-detail-arrow-up')
const productDetailArrowDown = document.querySelector('.product-detail-arrow-down')

productDetailToggleBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const element = e.currentTarget
        if(element.classList.contains('product-description-drop')){
            if(productDescription.classList.contains('hide-product-description')){
                productDescription.classList.remove('hide-product-description')
                productDescriptionArrowDown.style.display = 'none'
                productDescriptionArrowUp.style.display = 'flex'
            }else{
                productDescription.classList.add('hide-product-description')
                productDescriptionArrowDown.style.display = 'flex'
                productDescriptionArrowUp.style.display = 'none'
            }
        }else if(element.classList.contains('product-detail-drop')) {
            if(productDetail.classList.contains('hide-product-detail')) {
                productDetail.classList.remove('hide-product-detail')
                productDetailArrowDown.style.display = 'none'
                productDetailArrowUp.style.display = 'flex'
            }else {
                productDetail.classList.add('hide-product-detail')
                productDetailArrowDown.style.display = 'flex'
                productDetailArrowUp.style.display = 'none'
            }
        }
    })
})


/*
=================================
PRODUCT DETAIL PAGE EXTRAN IMAGES
=================================
*/ 
const productDetailExtraImage = [...document.querySelectorAll('.product-detail-extra-image')]

productDetailExtraImage.forEach((img) => {
    img.addEventListener('click', (e) => {
        const targetElement = e.currentTarget
        const childElement = targetElement.querySelector('.extra-image')
        const closeBtn = targetElement.querySelector('.product-detail-image-close-btn')
        if(!targetElement.classList.contains('extra-image-full-screen')){
            targetElement.classList.add('extra-image-full-screen')
            childElement.classList.add('image-full-screen')
            body.style.overflow = 'hidden'
            closeBtn.style.display = 'block'
        }else{
            targetElement.classList.remove('extra-image-full-screen')
            childElement.classList.remove('image-full-screen')
            body.style.overflow = 'auto'
            closeBtn.style.display = 'none'
        }
        
        
    })
})


