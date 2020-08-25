const app = new Vue({
  el: "#app",
  data: {
    error: null,
    short_url: null
  },
  computed: {
    shortUrlLink: function() {
      return `/${this.short_url}`
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

      const { error, short_url } = await response.json();
      this.error = error;
      this.short_url = short_url;
    },
    copyShortUrl() {
      const shortUrl = document.querySelector(".short-url").href;
      navigator.clipboard.writeText(shortUrl);
    }
  }
});
