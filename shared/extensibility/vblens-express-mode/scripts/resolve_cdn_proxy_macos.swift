#!/usr/bin/env swift

import Foundation
import CFNetwork

private let approvedHosts = Set(["static.oracle.com", "static-stage.oracle.com"])

private enum ProxyResolutionError: Error {
  case invalidTarget
  case systemSettingsUnavailable
  case invalidPacConfiguration
  case pacDownloadFailed
  case pacEvaluationFailed
  case unsupportedProxy
}

private func emit(_ payload: [String: Any]) throws {
  let data = try JSONSerialization.data(withJSONObject: payload, options: [.sortedKeys])
  guard let output = String(data: data, encoding: .utf8) else {
    throw ProxyResolutionError.pacEvaluationFailed
  }
  print(output)
}

private func proxyDictionary(_ value: Any) -> [AnyHashable: Any]? {
  value as? [AnyHashable: Any]
}

private func proxyType(_ dictionary: [AnyHashable: Any]) -> String? {
  dictionary[kCFProxyTypeKey] as? String
}

private func evaluatePac(_ url: URL, _ dictionary: [AnyHashable: Any]) throws -> [Any] {
  guard let pacURL = dictionary[kCFProxyAutoConfigurationURLKey] as? URL,
        pacURL.scheme == "http" || pacURL.scheme == "https",
        pacURL.user == nil,
        pacURL.password == nil else {
    throw ProxyResolutionError.invalidPacConfiguration
  }
  let script: String
  do {
    script = try String(contentsOf: pacURL, encoding: .utf8)
  } catch {
    throw ProxyResolutionError.pacDownloadFailed
  }
  guard let evaluated = CFNetworkCopyProxiesForAutoConfigurationScript(
    script as CFString,
    url as CFURL,
    nil
  )?.takeRetainedValue() as? [Any] else {
    throw ProxyResolutionError.pacEvaluationFailed
  }
  return evaluated
}

private func resolvedEntries(_ url: URL) throws -> [Any] {
  guard let settings = CFNetworkCopySystemProxySettings()?.takeRetainedValue(),
        let entries = CFNetworkCopyProxiesForURL(
          url as CFURL,
          settings
        ).takeRetainedValue() as? [Any] else {
    throw ProxyResolutionError.systemSettingsUnavailable
  }
  for entry in entries {
    guard let dictionary = proxyDictionary(entry) else { continue }
    if proxyType(dictionary) == (kCFProxyTypeAutoConfigurationURL as String) {
      return try evaluatePac(url, dictionary)
    }
  }
  return entries
}

private func resolve(_ url: URL) throws -> [String: Any] {
  for entry in try resolvedEntries(url) {
    guard let dictionary = proxyDictionary(entry), let type = proxyType(dictionary) else {
      continue
    }
    if type == (kCFProxyTypeNone as String) {
      return ["mode": "DIRECT", "source": "system"]
    }
    if type == (kCFProxyTypeHTTP as String) || type == (kCFProxyTypeHTTPS as String) {
      guard dictionary[kCFProxyUsernameKey] == nil,
            dictionary[kCFProxyPasswordKey] == nil,
            let host = dictionary[kCFProxyHostNameKey] as? String,
            !host.isEmpty,
            let port = dictionary[kCFProxyPortNumberKey] as? NSNumber,
            port.intValue > 0,
            port.intValue <= 65_535 else {
        throw ProxyResolutionError.unsupportedProxy
      }
      return [
        "mode": "PROXY",
        "proxy": "http://\(host):\(port.intValue)",
        "source": "system"
      ]
    }
    throw ProxyResolutionError.unsupportedProxy
  }
  throw ProxyResolutionError.unsupportedProxy
}

do {
  guard CommandLine.arguments.count == 2,
        let target = URL(string: CommandLine.arguments[1]),
        target.scheme == "https",
        target.user == nil,
        target.password == nil,
        let host = target.host,
        approvedHosts.contains(host) else {
    throw ProxyResolutionError.invalidTarget
  }
  try emit(resolve(target))
} catch {
  FileHandle.standardError.write(Data("CDN proxy auto-resolution failed.\n".utf8))
  exit(1)
}
