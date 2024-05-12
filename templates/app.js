document.addEventListener('DOMContentLoaded', function() {
    const feed = document.getElementById('feed');
});

async function updateFeed() {
    const inputText = document.getElementById('tweet-input').value;
    const response = await fetch('/get-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: inputText})
    });

    const tweetURLs = await response.json();
    const feed = document.getElementById('feed');

    // Clear existing tweets
    feed.innerHTML = '';

    tweetURLs.forEach(url => {
        let tweetEmbed = document.createElement('blockquote');
        tweetEmbed.className = 'twitter-tweet';
        tweetEmbed.innerHTML = `<a href="${url}"></a>`;
        feed.appendChild(tweetEmbed);
    });

    // Reload Twitter widgets to render tweets
    twttr.widgets.load();
}
