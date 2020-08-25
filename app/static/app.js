const app = new Vue({
  el: "#app",
  data: {
    output: null
  },
  methods: {
    async getShortUrl(url, expiration_date = null) {
      const response = await fetch("/new", {
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ url, expiration_date })
      });
      const json = await response.json();
      this.output = json["error"] || json["short_url"]
    }
  }
});
