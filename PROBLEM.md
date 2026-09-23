# Problem Statement

## Why is this a problem?

Most modern learning tools assume a fast, always-on internet connection. Online courses, search engines, and cloud AI assistants all stop working the moment connectivity drops. In large parts of rural Africa, connectivity is not just slow or intermittent. It is often absent, or so expensive per megabyte that using it for learning is not realistic.

The result is an information gap that compounds. A farmer who cannot look up the right maize variety for their rainfall zone plants the wrong one. A young person who has never been shown how mobile money scams work loses their savings. A small trader who does not know a government agrifinance scheme exists never applies. The knowledge to avoid each of these outcomes already exists in written form. What is missing is a way to deliver it, in plain language, at the moment someone has the question.

## Who experiences it?

- **Students in rural schools** that have no internet connection, or a single shared connection too weak for a classroom.
- **Smallholder farmers** who own a basic smartphone but cannot afford data for anything beyond messaging.
- **Small business owners and traders** trying to understand loan products, application steps, and government support schemes.
- **Teachers and community centre staff** who want to offer guided, question-driven learning but have no tools that work offline.
- **NGOs and agricultural extension workers** who need a low-cost way to leave reliable, self-service information behind after a visit.

## Why does it matter now?

Three things have changed recently:

1. **Small language models are now good enough to run on cheap hardware.** A 1.5 billion parameter model like Qwen 2.5 runs on a Raspberry Pi 5 and answers a question in a few seconds. Two years ago this required a cloud GPU.
2. **Smartphone ownership has outpaced connectivity.** Many people who cannot afford data still carry a phone with a browser. A local WiFi hotspot turns that phone into a learning terminal without installing anything.
3. **Food security and financial inclusion are urgent.** Climate variability is making traditional farming knowledge less reliable, and mobile financial services are expanding faster than the digital literacy needed to use them safely. Both create a demand for trustworthy, up-to-date guidance right now.

## What are we trying to change?

We want to make it normal for a school, farm cooperative, or community centre to own a small box that answers questions from a curated, locally relevant knowledge base, with no internet and no recurring cost.

Concretely, the project aims to:

- Turn a Raspberry Pi and its built-in WiFi into a shared, offline AI tutor for a whole room of people.
- Ground every answer in vetted local content so that teachers control what the assistant knows, rather than relying on a general model's guesses.
- Let non-technical staff add or update knowledge by dropping a text file into a folder.
- Keep the total hardware cost low enough that an NGO or school can deploy several units.
- Extend to local languages, starting with Swahili, so the barrier is not English fluency.

Success looks like a student or farmer walking up with a question, connecting their phone, and getting a clear, correct, practical answer in under ten seconds, with no data plan and no internet.
