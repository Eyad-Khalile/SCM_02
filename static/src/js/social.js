// WHATSAPP
// https://api.whatsapp.com/send?text=[post-title] [post-url]

// FACEBOK 
// https://www.facebook.com/sharer.php?u=[post-url]

// TWITTER
// https://twitter.com/share?url=[post-url]&text=[post-title]&via=[via]&hashtags=[hashtags]

// LINKEDIN 
// https://www.linkedin.com/shareArticle?url=[post-url]&title=[post-title]

const facebookBtn = $('.facebook-btn');
const twitterBtn = $('.twitter-btn');
const linkedinkBtn = $('.linkedin-btn');
const whatsappBtn = $('.whatsapp-btn');

function init() {
    let url = encodeURI(document.location.href);
    let post_title = encodeURI($('#post_title').text());
    let image = encodeURI($('#post_img').attr('src'));
    let description = encodeURI($('#post_content').text());
    
    facebookBtn.attr(
        'href',
        `https://www.facebook.com/sharer.php?u=${url}&text=${post_title}&image=${image}`
    );
    twitterBtn.attr(
        'href',
        `https://twitter.com/share?url=${url}&text=${post_title}`
    );
    linkedinkBtn.attr(
        'href',
        `https://www.linkedin.com/shareArticle?url=${url}&title=${post_title}`
    );
    whatsappBtn.attr(
        'href',
        `https://api.whatsapp.com/send?text=${post_title} ${url}`
    );

    
}
init();