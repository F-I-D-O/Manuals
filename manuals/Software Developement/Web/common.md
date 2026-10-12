# Domain Name System (DNS)

- [Wikipedia](https://en.wikipedia.org/wiki/Domain_Name_System)
- [List of DNS record types](https://en.wikipedia.org/wiki/List_of_DNS_record_types)
- [RFC 1034](https://www.rfc-editor.org/info/rfc1034/) (Domain names - concepts and facilities)
- [RFC 1035](https://www.rfc-editor.org/info/rfc1035/) (Domain names - implementation and specification)

Domain name system is a system that associates domain names with other information. The most important information is the IP address of the server that serves the URLs with the domain name (i.e., hosts the domain).

Each DNS record has the following format:

```txt
<domain name> <type> <class> <ttl> <data>
```

where:

- `<type>` is one of the predefined record types (see below),
- `<class>`
- `<ttl>` is the time to live, i.e., how long the DNS server may cache the old record after the record is changed.

Over time, the DNS system expanded to store other types of mapping than just domain -> IP address. The most common record types are:

- **A (IPv4)**: maps a domain name to an IPv4 address
- **AAAA (IPv6)**: maps a domain name to an IPv6 address
- [**CNAME (canonical name)**](https://en.wikipedia.org/wiki/CNAME_record): domain name alias. Maps name to another domain name instead of an IP address.
- [**TXT (text)**](https://en.wikipedia.org/wiki/TXT_record): Arbitrary text. Typically stores machine readable information for servicis such as domain ownership verification.

Note that different DNS severs may have different records for the same domain name, e.g., based on geographical location. This enables routing various users to different servers simultaneously.

DNS records are hierarchical and the domain name resolution is done by prepending the domain name from the record to the current origin. In the top-level DNS, the current origin is empty, but e.g., a DNS table for `fido.ninja` resolves domain name `www` to `www.fido.ninja`. and `fido` to `fido.fido.ninja`.

The name server is supposed to return the record if an exact match exists. If it does not, it also checks for a [wildcard record](https://www.rfc-editor.org/info/rfc1034/#section-4.3.3). For example, if `a.fido.ninja` is not defined, but `*.fido.ninja` is, the name server returns the record for `*.fido.ninja`. Note however that `*.fido.ninja` does not cover the domain itself, i.e., `fido.ninja` is still not resolved.

The [formatting of the DNS record](https://www.rfc-editor.org/info/rfc1035/#section-5.1) is mostly irrelevant for the end user, with exception of the `@` sign that is wildly used in the domain name. The `@` sign is replaced by the current origin, e.g., at `fido.ninja`, the record `@` resolves to `fido.ninja`.


# URL Redirection
[Wikipedia](https://en.wikipedia.org/wiki/URL_redirection)

Redirection is a mechanism that allows the client (e.g., web browser) to redirect the request to a different URL. There are several types of redirection, here ordered from the lowest level (early) to the highest level (late):

1. **Domain provider redirection**: Domenin provider inserts an A record pointing to its own redirection server. This server maps the original domain to the new domain.
    - on Namecheap, this is named `URL Redirect Record`
1. **.htaccess redirection**: the HTTP server (Apache, nginx, etc.) can redirect the request to a different URL using the `.htaccess` file.
1. **backend redirection**: the server code (e.g., PHP, server-side JavaScript, Python, etc.) redirects the request
1. **HTML redirection**: two mechanisms exist:
    - [**meta refresh**](https://en.wikipedia.org/wiki/URL_redirection#Refresh_Meta_tag_and_HTTP_refresh_header): `<meta http-equiv="refresh" ..>` tag may be used to redirect the request to a different URL.
    - [**iframe**](https://en.wikipedia.org/wiki/URL_redirection#Frame_redirects)
1. [**JavaScript redirection**](https://en.wikipedia.org/wiki/URL_redirection#JavaScript_redirects): after the page is loaded, the Frontend JavaScript code can redirect the request to a different URL.
1. **Manual redirection**: User is prompted to click a redirection link.

Redirections 1, 2, and sometimes 3 are realize using a standardized HTTP redirection, i.e., the HTTP header contains the redirection status. Various [status codes](https://en.wikipedia.org/wiki/URL_redirection#HTTP_status_codes_3xx) are used, each for a different type of redirection.