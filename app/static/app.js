const app = new Vue({
  el: "#app",
  data: {
    error: null,
    shortUrl: null
  },
  computed: {
    shortUrlLink: function() {
      return `/${this.shortUrl}`;
    }
  },
  methods: {
    async getShortUrl() {
      const url = document.getElementById("url").value;
      const alias = document.getElementById("alias").value;

      const date = document.getElementById("date").value;
      const time = document.getElementById("time").value;

      const expirationDate = date
        ? new Date(`${date} ${time}`).toISOString()
        : null;

      const response = await fetch("/new", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ url, alias, expirationDate })
      });

      const { error, shortUrl } = await response.json();
      this.error = error;
      this.shortUrl = shortUrl;
    },
    copyShortUrl() {
      const shortUrl = document.querySelector(".short-url").href;
      navigator.clipboard.writeText(shortUrl);
    },
    today() {
      return new Date().toISOString();
    },
    currentDate() {
      return this.today().slice(0, 10);
    },
    currentTime() {
      return this.today().slice(11);
    }
  }
});
