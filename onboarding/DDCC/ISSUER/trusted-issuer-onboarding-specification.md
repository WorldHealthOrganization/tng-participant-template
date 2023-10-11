# Trusted Issuer

Other credential types like Verifiable Credentials are using DIDs or other Issuer IDs which are not necessarily linked to any SCA, but with crypto material behind it. 
To support these issuers and their credentials, trusted issuers must be onboarded like SCAs and all other certificates.
For the onboarding a JSON structure is used.

## JSON structure specification

The JSON structure is defined as follows named `trusted-issuer.json`:

```json
{
  "name": "Ministry of Health",
  "url": "did:web:example.com",
  "urlType": "DID",
  "hash": "463bcd43a6ae45a5d9606adfb0c2d968cfacb73e0df827f05a7c7f781a1869c5",
  "sslPublicKeys": [
    "MIIGwjCCBaqgAwIBAvd3QuY29tMEkGCCsG....Lz3lGqBrHBklHq7x5WK4dAipTLrG39u",
    "MIIGwjCCBaqgAwIBAvd3QuY29tMEkGCCsG....Lz3lGqBrHBklHq7x5WK4dAipTLrG40u"
  ]
}
```

Multiple files can be provided by adding a numbered suffix like `trusted-issuer_1.json`, `trusted-issuer_2.json`.


| Field         | Optional | Type   | constraints          | Description                                                                                                                                                 |
|---------------|----------|--------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name          | No       | String | 512 chars            | Name of the Service                                                                                                                                         |
| url           | No       | String | 64 chars             | A resolvable DID URL using did:web as DID method                                                                                                            |
| urlType       | No       | String | 25 chars             | DID                                                                                                                                                         |
| hash          | No       | String | 64 chars             | SHA256 Hash of the content behind it (if applicable)                                                                                                        |
| sslPublicKeys | No       | String | 2048 chars per entry | SSL Certificates of the endpoint hosting the DID document. Additional entry may be used to support key rotation. (Format: Base64 of the DER representation) |

The JSON structure will be signed by the trust anchor and onboarded to the gateway.
