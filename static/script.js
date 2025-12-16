const searchMessages = [
    "Searching the universe 🌌",
    "Scanning distant galaxies ✨",
    "Exploring Andromeda 🌀",
    "Aligning quantum vectors 🧠",
    "Finding cinematic matches 🎬"
];

let textInterval;

function showOverlay() {
    const overlay = document.getElementById("overlay");
    const textEl = document.getElementById("searchText");

    overlay.classList.remove("hidden");
    let i = 0;
    textEl.innerText = searchMessages[i];

    textInterval = setInterval(() => {
        i = (i + 1) % searchMessages.length;
        textEl.innerText = searchMessages[i];
    }, 1200);
}

function hideOverlay() {
    clearInterval(textInterval);
    document.getElementById("overlay").classList.add("hidden");
}

async function getRecommendations() {
    const query = document.getElementById("movieInput").value.trim();
    if (!query) return;

    showOverlay();

    const url = "/movie-result";

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_des: query
            })
        });

        if (!res.ok) throw new Error("Request failed");

        const data = await res.json();
        displayResults(data);
    } catch (err) {
        console.error(err);
        alert("Something went wrong. Try again.");
    } finally {
        hideOverlay();
    }
}

function displayResults(movies) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";

        if (movie.poster) {
            const img = document.createElement("img");
            img.src = movie.poster;
            img.alt = movie.title;

            img.onerror = () => {
                img.remove();
                const msg = document.createElement("div");
                msg.className = "no-poster";
                msg.innerText = "Sorry\nPoster not available";
                card.prepend(msg);
            };

            card.appendChild(img);
        }

        const title = document.createElement("div");
        title.className = "movie-title";
        title.innerText = movie.title;

        card.appendChild(title);
        container.appendChild(card);
    });
}
