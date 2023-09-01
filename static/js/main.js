const scrollBtns = document.querySelector('.scroll-btns')
const scrollDown = document.querySelector('.scroll-down')
const scrollUp = document.querySelector('.scroll-up')
const bodyWidth = document.querySelector('body')

const mobileNavs = [...document.querySelectorAll('.mobile-nav')]
const mobileNavLinks = document.querySelector('.mobile-nav-links')
const mobileNavCloseBtn = document.querySelector('.mobile-nav-close-btn')
const mobileToggleNavBtn = document.querySelector('.mobile-toggle-nav-btn')
const mobileNavBackgroundLayout = document.querySelector('.mobile-nav-background-layout')
const mobileNavLinkSearchButton = document.querySelector('.mobile-nav-link-search-button')


const navLinkSearchButton = document.querySelector('.nav-link-search-button')
const searchIcon = document.querySelector('.search-icon')
const searchFormWrapper = document.querySelector('.search-form-wrapper')
const searchFormCloseButton = document.querySelector('.search-form-close-btn')

const toggleUserNavbar = document.querySelector('.toggle-user-navbar')
const loggedInUserNavLinks = document.querySelector('.logged-in-user-nav-links')
const loggedInNavbarArrowUp = document.querySelector('.logged-in-navbar-arrow-up')
const loggedInNavbarArrowDown = document.querySelector('.logged-in-navbar-arrow-down')
const loggedInNavbarUsername = document.querySelector('.logged-in-navbar-username')
const loggedInNavbarUserProfileImg = document.querySelector('.logged-in-navbar-user-profile-img')

const bannerImgContainers = [...document.querySelectorAll('.banner-img-container')]
const bannerArrowLeft = document.querySelector('.banner-arrow-left')
const bannerArrowRight = document.querySelector('.banner-arrow-right')
const TranslateBtns = [...document.querySelectorAll('.translate-btn')]
const circles = [...document.querySelectorAll('.circle')]

const productDetailToggleBtns = [...document.querySelectorAll('.product-detail-toggle-btn')]
const productDescription = document.querySelector('.product-description')
const productDetail = document.querySelector('.product-detail')
const productDescriptionArrowUp = document.querySelector('.product-description-arrow-up')
const productDescriptionArrowDown = document.querySelector('.product-description-arrow-down')
const productDetailArrowUp = document.querySelector('.product-detail-arrow-up')
const productDetailArrowDown = document.querySelector('.product-detail-arrow-down')
const productDetailExtraImage = [...document.querySelectorAll('.product-detail-extra-image')]

const body = document.querySelector('body')

/*
==================
SCROLL UP AND DOWN
==================
*/ 

if((window.innerWidth - bodyWidth.clientWidth)/2 != 0) {
    scrollBtns.style.right = `${(window.innerWidth - bodyWidth.clientWidth)/2}px`
}

if(scrollDown && scrollUp) {
    window.addEventListener('scroll', (e) => {
        if(window.pageYOffset === 0) {
            scrollDown.style.display = 'none'
            scrollUp.style.display = 'none'
        }
        else if(window.pageYOffset >= 300) {
            scrollDown.style.display = 'none'
            scrollUp.style.display = 'flex'
        }else if(window.pageYOffset <= 300 && window.pageYOffset > 0) {
            scrollDown.style.display = 'flex'
            scrollUp.style.display = 'none'
        }
    })

    window.addEventListener('resize', (e) => {
        if((window.innerWidth - bodyWidth.clientWidth)/2 != 0) {
            scrollBtns.style.right = `${(window.innerWidth - bodyWidth.clientWidth)/2}px`
        }
    })
}



/*
================
MOBILE NAV LINKS
================
*/ 

mobileToggleNavBtn.addEventListener('click', (e) => {
    searchFormWrapper.classList.remove('show-search-form-wrapper')
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
================
DESKTOP NAV LINKS
================
*/ 

if (toggleUserNavbar) {
    toggleUserNavbar.addEventListener('click', (e) => {
        searchFormWrapper.classList.remove('show-search-form-wrapper')
        loggedInUserNavLinks.classList.toggle('show-logged-in-user-nav-links')
        if(loggedInUserNavLinks.classList.contains('show-logged-in-user-nav-links')){
            loggedInNavbarArrowUp.style.display = 'flex'
            loggedInNavbarArrowDown.style.display = 'none'
        }else{
            loggedInNavbarArrowUp.style.display = 'none'
            loggedInNavbarArrowDown.style.display = 'flex'
        }
    })
}


navLinkSearchButton.addEventListener('click', (e) => {
    searchFormWrapper.classList.toggle('show-search-form-wrapper')
})

searchFormCloseButton.addEventListener('click', (e) => {
    searchFormWrapper.classList.toggle('show-search-form-wrapper')
})

mobileNavLinkSearchButton.addEventListener('click', (e) => {
    searchFormWrapper.classList.toggle('show-search-form-wrapper')
    mobileNavLinks.classList.remove('show-mobile-nav-bar')
    mobileNavBackgroundLayout.style.display = 'none'
    body.style.overflow = 'auto'

})


window.addEventListener('click', (e) => {
    if(e.target != loggedInNavbarUserProfileImg &&
        e.target != loggedInNavbarUsername &&
        e.target != loggedInNavbarArrowUp &&
        e.target != loggedInNavbarArrowDown
    ){
        if(!loggedInUserNavLinks.classList.contains('show-logged-in-user-nav-links')) {
            loggedInNavbarArrowUp.style.display = 'none'
            loggedInNavbarArrowDown.style.display = 'flex'
        }
        else {
            loggedInUserNavLinks.classList.remove('show-logged-in-user-nav-links')
            loggedInNavbarArrowUp.style.display = 'none'
            loggedInNavbarArrowDown.style.display = 'flex'
        }
    }
})

window.addEventListener('resize', (e) => {
    // searchFormWrapper.classList.remove('show-search-form-wrapper')
    if(loggedInUserNavLinks){
        loggedInUserNavLinks.classList.remove('show-logged-in-user-nav-links')
    }
    mobileNavLinks.classList.remove('show-mobile-nav-bar')
    mobileNavBackgroundLayout.style.display = 'none'
    body.style.overflow = 'auto'
})
/*
=============
BANNER IMAGES
=============
*/

const largeScreen = ['pc.webp', 'monitor.webp', 'laptop.webp']
const mobileScreen = ['pc-small.webp', 'monitor-small.webp', 'laptop-small.webp']

if(window.innerWidth > 910) {
    bannerImgContainers.forEach((container, index) => {
        const img = container.querySelector('img') 
        let src = `/static/images/${largeScreen[index]}`
        img.setAttribute('src', src)
    })
}else if(window.innerWidth < 910) {
    bannerImgContainers.forEach((container, index) => {
        let img = container.querySelector('img') 
        let src = `/static/images/${mobileScreen[index]}`
        img.setAttribute('src', src)
    })
}


window.addEventListener('resize', (e) => {
    if(window.innerWidth > 910) {
        bannerImgContainers.forEach((container, index) => {
            const img = container.querySelector('img') 
            let src = `/static/images/${largeScreen[index]}`
            img.setAttribute('src', src)
        })
    }else if(window.innerWidth < 910) {
        bannerImgContainers.forEach((container, index) => {
            let img = container.querySelector('img') 
            let src = `/static/images/${mobileScreen[index]}`
            img.setAttribute('src', src)
        })
    }
})

let index = 0

if(circles && circles[0]) {
    circles[0].style.background = 'white'
}

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
            body.scrollTop(0)
        }else{
            targetElement.classList.remove('extra-image-full-screen')
            childElement.classList.remove('image-full-screen')
            body.style.overflow = 'auto'
            closeBtn.style.display = 'none'
        }
    })
})


