const app = new Vue({
  el: "#app",
  data: {
    error: null,
    shortUrl: null
  },
  computed: {
    shortUrlLink: function() {
      return `/${this.shortUrl}`
    },
  },
  methods: {
    async getShortUrl(url, alias) {
      url = document.getElementById("url").value;
      alias = document.getElementById("alias").value;

      const response = await fetch("/new", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ url, alias })
      });

      const { error, shortUrl } = await response.json();
      this.error = error;
      this.shortUrl = shortUrl;
    },
    copyShortUrl() {
      const shortUrl = document.querySelector(".short-url").href;
      navigator.clipboard.writeText(shortUrl);
    }
  }
});
