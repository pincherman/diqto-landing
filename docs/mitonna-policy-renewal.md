# Mitonna withdrawal policy: local source candidate only

## Existing publication evidence, 15 November 2026

Public repository PR #1 merged at 18:00:09 UTC, merge/main pin

diqto-landing@ef5ee8ceac4f462ecc1844c8c9458a166d0740e0.

At 18:13:30 UTC the fixed HTTPS policy endpoint returned HTTP 200 and the
same 200 bytes as main: schema 1, sequence 1, zero withdrawn IDs, issued
15 November 2026 13:42:12 UTC, expires 16 November 2026 13:42:12 UTC.
Observed response: GitHub.com, max-age=600, Age=0, JSON MIME. This establishes
static publication of that artifact, not a recurring renewal route, complete
Pages configuration or a publication latency SLA. Unauthenticated Pages API
returned 404, not proof of absence. Subsequent owner evidence relayed by Claude
at 18:17 UTC reports Pages legacy main:/, CNAME diqto.fr and a successful build;
its current publication executor is a GitHub-hosted runner, forbidden in this
task. That evidence was not independently inspected by this author. No
autonomous runner, versioned schedule or SITE cron was found in that owner
inspection; OpenClaw scheduling was not verified. No .github/workflows
or renewal producer exists in the inspected main tree. The internal GitHub
Pages inventory remains in the previous private deliverable, intentionally not
restored to the public site (PR #1 removed it before merge).

## Candidate

The local tool explicitly reissues a previously trusted policy even while it
is valid; unlike the app producer's previous valid/no-change no-op:

* issuedAt is captured from the real clock under the local writer lock;
* sequence increments exactly once, overflow and clock rollback refuse;
* expiry is exactly now+86400. A previous TTL above 86400 is refused;
* withdrawnIDs including order, schema, manifest and reason remain unchanged;
* no creation from an absent policy, reset to N=0, additions or removal of IDs;
* stable advisory flock plus expected source SHA256 and atomic fsync/replace
  serialize cooperating local writers. Old SHA loses, without automatic retry.

The tool requires a previously consumer-qualified policy from the authoritative
site revision; it validates shape, pinned manifest and ID syntax, but does NOT
establish ID membership or source authenticity by itself. The existing pinned
catalogue/consumer must validate the candidate before any eventual publication.
Do not use an arbitrary downloaded policy or stale checkout as authority.

The advisory deadline begins six hours before expiry. For the currently
published sequence 1 this is 16 November 2026 07:42:12 UTC. Start early enough
to leave time for owner approval, publication and the observed 600-second CDN
cache; six hours is a safety margin, not a promise about infrastructure. A future
operator must verify fresh remote bytes before expiry. Never extend the TTL to
hide a missed renewal. At expiry the existing app's fail-closed behavior is
unchanged; this candidate neither changes nor requalifies it.

Local usage on an authorized working-copy policy, not production:


env M20_TEST_TMPDIR=<declared-scratch-directory> python3 -B -m unittest discover -s tests -p test_renew_mitonna_withdrawals.py -v

python3 -B tools/renew_mitonna_withdrawals.py --policy <local-policy> --expected-sha256 <reviewed-current-sha256> --check-due

python3 -B tools/renew_mitonna_withdrawals.py --policy <local-policy> --expected-sha256 <reviewed-current-sha256>

--check-due is read-only (0 not due, 3 due/expired); explicit renewal always
reissues. These commands do not push, publish or schedule anything. Keep the
stable dot-lock untracked and never remove it while writers could exist.

## BLOCKED: operational renewal/publication not qualified

Owner action via Claude/Ronin: identify an EXISTING authorized SITE-only
renewal/publication route WITHOUT a GitHub-hosted runner, plus its remote ref
CAS and single-writer protocol. No such route has been demonstrated. SITE-only
push access exists with Ronin B21a, who can collect this source after independent
PASS; this author did not receive or use those credentials. The known Pages
source main:/ and access do not qualify unattended renewal. A source commit,
local lock or HTTP GET is not that proof.
Do not invent a cron, hosted Actions runner, token or alternative deploy path.
No push/PR creation, merge, publication, scheduler activation, new credentials,
app edit, build 988, allergens or costs are part of this candidate.

Before any separately authorized publication, the owner must fetch and compare
the authoritative remote policy/ref, preserve all tombstones and highest sequence,
review the exact candidate, perform the existing remote CAS publication route,
then GET exact JSON/MIME/sequence/timestamps before expiration. Any remote change
means stop and rebase/review, never overwrite with a force or stale CAS. A rollback
must NOT republish older policy bytes/sequence or restore withdrawn IDs; stop and
use an additive higher-sequence correction under the same qualified owner route.

Until that route is supplied and qualified, operational renewal is BLOCKED,
no job runs in the background and the tracked sequence-1 policy is unchanged.
