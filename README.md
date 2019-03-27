sana.mds
========
Test 2.

This commit is pushed by Sebastián Felipe Landínez García.

I've found that in the lines I've changed, the MDS attached its session ID as a header. This gave me error 400: Bad Request, when doing a
request for a patient list. I red some of the documentation of OpenMRS, particularly the one of the authentication, and here it's said
that the session ID must be sent as a Cookie with the key jsessionid. Here's the change I've made, I put it as a header, but with the 
header name Cookie and setting the cookie value to jsessionid=//The session ID. This new request produced the following error response:

401: Not authorized.

It's not an solved issue but I think maybe you've passed through it without realizing. Maybe OpenMRS API is crashing?

Hope the commit is useful for you.
