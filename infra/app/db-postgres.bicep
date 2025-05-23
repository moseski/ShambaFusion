param serverName string
param location string = resourceGroup().location
param tags object = {}

param keyVaultName string

param databaseUser string = 'psqladmin'
param databaseName string = 'shamba_db'
@secure()
param databasePassword string

param allowAllIPsFirewall bool = false

resource postgreServer'Microsoft.DBforPostgreSQL/flexibleServers@2022-01-20-preview' = {
  location: location
  tags: tags
  name: serverName
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    version: '13'
    administratorLogin: databaseUser
    administratorLoginPassword: databasePassword
    storage: {
      storageSizeGB: 128
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    maintenanceWindow: {
      customWindow: 'Disabled'
      dayOfWeek: 0
      startHour: 0
      startMinute: 0
    }
  }

  resource firewall_all 'firewallRules' = if (allowAllIPsFirewall) {
    name: 'allow-all-IPs'
    properties: {
      startIpAddress: '0.0.0.0'
      endIpAddress: '255.255.255.255'
    }
  }
}

resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-01-20-preview' = {
  parent: postgreServer
  name: databaseName
  properties: {
    // Azure defaults to UTF-8 encoding, override if required.
    // charset: 'string' 
    // collation: 'string'
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

resource dbPasswordKey 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  parent: keyVault
  name: 'databasePassword'
  properties: {
    value: databasePassword
  }
}

output databaseHost string = postgreServer.properties.fullyQualifiedDomainName
output databaseName string = databaseName
output databaseUser string = databaseUser
output databaseConnectionKey string = 'databasePassword'
