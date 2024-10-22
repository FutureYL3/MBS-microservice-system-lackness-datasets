# 微服务系统缺陷收集

## [spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)

### Release：Dec 29, 2023 - now

#### Issue #259
**title**: Zipkin not showing traces
**url**: https://github.com/spring-petclinic/spring-petclinic-microservices/issues/259
**创建时间**: 2024-04-17T13:25:26+00:00, **更新时间**: 2024-04-21T17:54:08+00:00
**提出原因摘要**:
> **Bug描述**：在Windows 11系统上，通过Docker构建并启动应用后，日志正常但Zipkin未显示任何追踪信息。
> 
> **可能相关因素**：
> 1. Docker打包配置问题，特别是指定的`linux/arm64`平台。
> 2. Docker环境与应用之间的兼容性问题。
> 3. Zipkin配置或网络连接问题。
> 
> **可能的解决途径**：
> 1. 尝试在未使用Docker的情况下启动应用，验证问题是否依然存在。
> 2. 检查Docker构建和运行配置，确保`linux/arm64`平台设置正确。
> 3. 核实Zipkin的配置，包括服务地址和端口是否正确，确保网络通信正常。
> 4. 查看相关日志，排查Zipkin客户端与服务端之间的通信错误。
#### PR #264
**title**: Bump to Chaos Monkey 3.1.0
**url**: https://github.com/spring-petclinic/spring-petclinic-microservices/pull/264
**创建时间**: 2024-05-26T14:39:22+00:00, **更新时间**: 2024-08-02T08:10:32+00:00
**提出原因摘要**:
> **Bug描述**：Spring Petclinic微服务项目中存在代码质量问题，具体由@Ivan-Bobrov在讨论#262中提出。
> 
> **可能关联**：代码重复、测试覆盖率不足或潜在的安全漏洞等代码质量相关问题。
> 
> **解决途径**：通过提交并合并PR #264，按照SonarCloud的反馈优化代码，确保代码质量达到标准。
#### PR #255
**title**: Fix docker build on BTRFS
**url**: https://github.com/spring-petclinic/spring-petclinic-microservices/pull/255
**创建时间**: 2024-03-04T13:56:57+00:00, **更新时间**: 2024-03-04T14:22:54+00:00
**提出原因摘要**:
> 该bug是在使用BTRFS文件系统和Docker版本25.0.3时，运行`./mvnw clean install -PbuildDocker -Dmaven.test.skip=true`命令导致Docker构建过程失败，错误原因为“layer does not exist”。问题可能与Docker在BTRFS（以及类似的NTFS）文件系统上处理层的方式有关。解决途径包括修改Dockerfile以兼容相关文件系统，参考相关修复方案或调整文件系统配置。
