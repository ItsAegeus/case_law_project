const BASE_URL = "https://your-backend-url.com";

export const searchCaseLaw = async (keywords, jurisdiction) => {
    const response = await fetch(`${BASE_URL}/search/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keywords, jurisdiction }),
    });
    return response.json();
};
