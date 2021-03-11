import hvac

client = hvac.Client(url="http://127.0.0.1:8200")


read_response = client.sys.read_init_status()
print("Vault initialize status: %s" % read_response["initialized"])


print("Vault initialize status: %s" % client.sys.is_initialized())


"""
init_result = client.sys.initialize()

root_token = init_result['root_token']
unseal_keys = init_result['keys']

print("root =>", root_token)
print("unseal keys", unseal_keys)

client.sys.submit_unseal_keys(keys=unseal_keys)
"""

client.token = "s.vdStvMVThl8HfFndTesLRinzs.vdStvMVThl8HfFndTesLRinz"  # root_token
print("Is Vault sealed: %s" % client.sys.is_sealed())
methods = client.sys.list_auth_methods()
print("auth methods", methods)
